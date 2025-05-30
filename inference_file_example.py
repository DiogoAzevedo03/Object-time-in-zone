import argparse
from typing import List

import cv2
import numpy as np
from inference import get_model
from utils.general import find_in_list, load_zones_config
from utils.timers import FPSBasedTimer

import supervision as sv

COLORS = sv.ColorPalette.from_hex(["#E6194B", "#3CB44B", "#FFE119", "#3C76D1"])
COLOR_ANNOTATOR = sv.ColorAnnotator(color=COLORS)
LABEL_ANNOTATOR = sv.LabelAnnotator(
    color=COLORS, text_color=sv.Color.from_hex("#000000")
)


def main(
    source_video_path: str,
    zone_configuration_path: str,
    model_id: str,
    confidence: float,
    iou: float,
    classes: List[int],
) -> None:
    model = get_model(model_id=model_id)
    tracker = sv.ByteTrack(minimum_matching_threshold=0.5)
    video_info = sv.VideoInfo.from_video_path(video_path=source_video_path)
    frames_generator = sv.get_video_frames_generator(source_video_path)

    polygons = load_zones_config(file_path=zone_configuration_path)
    zones = [
        sv.PolygonZone(
            polygon=polygon,
            triggering_anchors=(sv.Position.CENTER,),
        )
        for polygon in polygons
    ]
    timers = [FPSBasedTimer(video_info.fps) for _ in zones]

    for frame in frames_generator:
        results = model.infer(frame, confidence=confidence, iou_threshold=iou)[0]
        detections = sv.Detections.from_inference(results)
        detections = detections[find_in_list(detections.class_id, classes)]
        detections = tracker.update_with_detections(detections)

        annotated_frame = frame.copy()

        for idx, zone in enumerate(zones):
            # Desenhar a zona - use o método .by_idx() do ColorPalette corretamente
            zone_color = COLORS.by_idx(idx % len(COLORS.colors))
            annotated_frame = sv.draw_polygon(
                scene=annotated_frame, 
                polygon=zone.polygon, 
                color=zone_color
            )

            detections_in_zone = detections[zone.trigger(detections)]
            time_in_zone = timers[idx].tick(detections_in_zone)

            # Filtrar apenas os que têm tracker_id válido (não None)
            valid_detections = []
            valid_times = []
            for i, tracker_id in enumerate(detections_in_zone.tracker_id):
                if tracker_id is not None:
                    valid_detections.append(i)
                    valid_times.append(time_in_zone[i])

            # Ignorar se não houver detecções válidas
            if len(valid_detections) == 0:
                continue

            detections_in_zone = detections_in_zone[valid_detections]
            time_in_zone = valid_times
            
            # Não passar cores personalizadas, deixar o COLOR_ANNOTATOR usar suas cores padrão
            annotated_frame = COLOR_ANNOTATOR.annotate(
                scene=annotated_frame,
                detections=detections_in_zone
            )

            labels = [
                f"#{tracker_id} {int(time // 60):02d}:{int(time % 60):02d}"
                for tracker_id, time in zip(detections_in_zone.tracker_id, time_in_zone)
            ]

            # Não passar cores personalizadas, deixar o LABEL_ANNOTATOR usar suas cores padrão
            annotated_frame = LABEL_ANNOTATOR.annotate(
                scene=annotated_frame,
                detections=detections_in_zone,
                labels=labels
            )
            
        cv2.imshow("Processed Video", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculating detections dwell time in zones, using video file."
    )
    parser.add_argument(
        "--zone_configuration_path",
        type=str,
        required=True,
        help="Path to the zone configuration JSON file.",
    )
    parser.add_argument(
        "--source_video_path",
        type=str,
        required=True,
        help="Path to the source video file.",
    )
    parser.add_argument(
        "--model_id", type=str, default="yolov8s-640", help="Roboflow model ID."
    )
    parser.add_argument(
        "--confidence_threshold",
        type=float,
        default=0.3,
        help="Confidence level for detections (0 to 1). Default is 0.3.",
    )
    parser.add_argument(
        "--iou_threshold",
        default=0.7,
        type=float,
        help="IOU threshold for non-max suppression. Default is 0.7.",
    )
    parser.add_argument(
        "--classes",
        nargs="*",
        type=int,
        default=[],
        help="List of class IDs to track. If empty, all classes are tracked.",
    )
    args = parser.parse_args()

    main(
        source_video_path=args.source_video_path,
        zone_configuration_path=args.zone_configuration_path,
        model_id=args.model_id,
        confidence=args.confidence_threshold,
        iou=args.iou_threshold,
        classes=args.classes,
    )