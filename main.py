import os
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

# --- Configuration ---
image_path = r"data\cadre-1.png"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# --- Initialisation du modèle OCR ---
ocr = PaddleOCR(
    use_angle_cls=True,  # détection d’orientation du texte
    lang='fr',           # modèle multi-langue (FR inclus)
    use_gpu=False        # ton PC perso n’a pas de GPU
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
text_output = os.path.join(output_dir, "exemple_bulletin_paye.txt")
with open(text_output, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"[OK] Résultats enregistrés dans {text_output}")

# --- Génération d'une image annotée ---
image = Image.open(image_path).convert('RGB')
boxes = [line[0] for region in result for line in region]
txts = [line[1][0] for region in result for line in region]
scores = [line[1][1] for region in result for line in region]

im_show = draw_ocr(image, boxes, txts, scores, font_path="C:\\Windows\\Fonts\\arial.ttf")
annotated_path = os.path.join(output_dir, "exemple_bulletin_paye_annotated.jpg")
im_show = Image.fromarray(im_show)
im_show.save(annotated_path)
print(f"[OK] Image annotée enregistrée dans {annotated_path}")
