# ⏱️ time in zone

Demonstração prática sobre como utilizar visão computacional para **analisar tempos de espera** e monitorizar **a duração que objetos ou pessoas passam em zonas pré-definidas** de vídeos.  
Este projeto de exemplo é ideal para aplicações como **análise de comportamento em lojas**.

---

## 💻 Instalação

1. Clone o repositório e navegue até ao diretório do exemplo:

   ```bash
   git clone --depth 1 -b develop https://github.com/DiogoAzevedo03/Object-time-in-zone.git
   cd supervision/examples/time_in_zone
   ```

2. Crie e ative um ambiente virtual Python *(opcional, mas recomendado)*:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠 Scripts

### `draw_zones`

Se quiser testar a análise de tempo em zonas com o seu próprio vídeo, pode utilizar este script para **desenhar zonas personalizadas** e guardar os resultados num ficheiro `.json`.  
Uma janela será aberta para permitir desenhar polígonos sobre uma imagem ou vídeo. Esses polígonos serão guardados como ficheiro de configuração.

Parâmetros:

- `--source_path`: Caminho para o vídeo ou imagem onde pretende desenhar os polígonos.
- `--zone_configuration_path`: Caminho onde será guardado o ficheiro JSON com os polígonos desenhados.

Atalhos no teclado:

- `enter` → Finaliza o polígono atual.
- `escape` → Cancela o polígono atual.
- `q` → Fecha a janela.
- `s` → Guarda o ficheiro de configuração das zonas.

Exemplos de uso:

```bash
python scripts/draw_zones.py \
    --source_path "data/checkout/video.mp4" \
    --zone_configuration_path "data/checkout/config.json"
```

---

## 🎬 Processamento de Vídeo e Streams

### `inference_file_example`

Este script executa **detecção de objetos num vídeo** utilizando um modelo Roboflow Inference.

Parâmetros:

- `--zone_configuration_path`: Caminho para o ficheiro `.json` com as zonas.
- `--source_video_path`: Caminho para o ficheiro de vídeo.
- `--model_id`: ID do modelo da Roboflow.
- `--classes`: Lista de IDs de classes a seguir (se deixar vazio, segue todas).
- `--confidence_threshold`: Confiança mínima para aceitar detecções (de `0` a `1`). Padrão: `0.3`.
- `--iou_threshold`: IOU mínimo para supressão de detecções sobrepostas. Padrão: `0.7`.

Exemplo (análise de caixa de supermercado):

```bash
python inference_file_example.py \
    --zone_configuration_path "data/checkout/config.json" \
    --source_video_path "data/checkout/video.mp4" \
    --model_id "yolov8x-640" \
    --classes 0 \
    --confidence_threshold 0.3 \
    --iou_threshold 0.7
```

---

## 📦 Funcionalidades Implementadas

- Contagem do tempo que cada ID permanece em cada zona.
- Agrupamento dos tempos por ID (vários registos do mesmo ID são somados).
- Suporte a múltiplas zonas.

---

## ✅ Resultados

O sistema demonstrou ser eficaz para:

- Detetar e seguir objetos em tempo real com YOLOv8.
- Calcular com precisão o tempo passado em zonas específicas.
- Visualizar facilmente o tracking com a biblioteca Supervision.

Pode ser usado em contextos como:

- Monitorização de filas em lojas.
- Análise de permanência em zonas de interesse.

---

## 🔮 Melhorias Futuras

- 📤 Exportar os tempos por ID e zona para ficheiros CSV ou base de dados.  
- 🧠 Suportar múltiplas classes (ex: pessoas, carros, etc.).  
- 🌐 Criar uma interface web para visualização ao vivo dos dados.  
- 🚨 Implementar alertas em tempo real quando um objeto excede um tempo limite numa zona.

---

## 🔗 GitHub

Repositório do projeto:  
👉 [https://github.com/DiogoAzevedo03/Object-time-in-zone](https://github.com/DiogoAzevedo03/Object-time-in-zone)

---

## 📚 Referências

- [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com)
- [Supervision Docs (Roboflow)](https://github.com/roboflow/supervision)
- [OpenCV Documentation](https://docs.opencv.org)