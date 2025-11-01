import os
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

# --- Configuration ---
image_path = r"data\cadre-1.png"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# --- Dossier local des modèles (modifie le chemin selon ton user si besoin) ---
model_root = r".paddleocr"

det_model_dir = os.path.join(model_root, "detection", "ch_PP-OCRv3_det_infer")
rec_model_dir = os.path.join(model_root, "recognition", "multilingual_PP-OCRv3_rec_infer")
cls_model_dir = os.path.join(model_root, "direction", "ch_ppocr_mobile_v2.0_cls_infer")

# --- Initialisation du modèle OCR (offline) ---
ocr = PaddleOCR(
    use_angle_cls=True,          # détection orientation
    lang='fr',                   # modèle multi-langue
    use_gpu=False,               # CPU only
    det_model_dir=det_model_dir, # dossier local
    rec_model_dir=rec_model_dir,
    cls_model_dir=cls_model_dir
)

# --- Lecture et OCR ---
print(f"[INFO] Lecture de {image_path} ...")
result = ocr.ocr(image_path, cls=True)

# --- Extraction du texte ---
lines = []
for region in result:
    for line in region:
        txt = line[1][0]
        conf = line[1][1]
        lines.append(f"{txt} (conf={conf:.2f})")

# --- Sauvegarde texte brut ---
text_output = os.path.join(output_dir, "cadre-1.txt")
with open(text_output, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"[OK] Résultats enregistrés dans {text_output}")

# --- Génération d'une image annotée ---
image = Image.open(image_path).convert('RGB')
boxes = [line[0] for region in result for line in region]
txts = [line[1][0] for region in result for line in region]
scores = [line[1][1] for region in result for line in region]

im_show = draw_ocr(image, boxes, txts, scores, font_path="C:\\Windows\\Fonts\\arial.ttf")
annotated_path = os.path.join(output_dir, "cadre-1_annotated.jpg")
im_show = Image.fromarray(im_show)
im_show.save(annotated_path)
print(f"[OK] Image annotée enregistrée dans {annotated_path}")
