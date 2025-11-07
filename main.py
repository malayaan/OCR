import os
from paddleocr import PaddleOCR
from PIL import Image, ImageDraw, ImageFont

# --- Configuration ---
image_path = os.path.join("data", "cadre-1.png")
output_dir = r'C:\Users\decroux paul\Documents\info\OCR\output'
os.makedirs(output_dir, exist_ok=True)

# --- Dossier local des modèles ---
model_root = r".paddleocr"

det_model_dir = os.path.join(model_root, "detection", "ch_PP-OCRv3_det_infer")
rec_model_dir = os.path.join(model_root, "recognition", "multilingual_PP-OCRv3_rec_infer")
cls_model_dir = os.path.join(model_root, "direction", "ch_ppocr_mobile_v2.0_cls_infer")

# --- Initialisation du modèle OCR (offline) ---
ocr = PaddleOCR(
    use_angle_cls=True,  # Active le modèle pour l'orientation du texte
    lang='fr',  # Langue du texte
    det_model_dir=det_model_dir,
    rec_model_dir=rec_model_dir,
    cls_model_dir=cls_model_dir,
    use_gpu=False  # Utilisation du GPU
)

# --- Lecture et OCR ---
print(f"[INFO] Lecture de {image_path} ...")
result = ocr.ocr(image_path, cls=True)

# --- Extraction du texte et ajout des coordonnées ---
lines = []
# Nous allons regrouper les boxes ayant les mêmes positions y
for region in result:
    for line in region:
        txt = line[1][0]  # Texte reconnu
        conf = line[1][1]  # Confiance du modèle
        box = line[0]  # Coordonnées du texte (box de détection)
        coordinates = ', '.join([f"({int(x)}, {int(y)})" for x, y in box])  # Formater les coordonnées (x, y)
        
        # Ajout du texte et des coordonnées dans le fichier
        lines.append({
            "text": txt,
            "conf": conf,
            "coordinates": box,
        })

# --- Trier les lignes par leur position verticale (y) ---
lines.sort(key=lambda x: min(y for _, y in x["coordinates"]))  # Trie par la première coordonnée y

# --- Sauvegarde texte brut --- 
text_output = os.path.join(output_dir, "cadre-1.txt")
with open(text_output, "w", encoding="utf-8") as f:
    for line in lines:
        txt = line["text"]
        conf = line["conf"]
        coordinates = ', '.join([f"({int(x)}, {int(y)})" for x, y in line["coordinates"]])  # Formater les coordonnées (x, y)
        f.write(f"Texte: {txt} (Confiance: {conf:.2f}) - Coordonnées: {coordinates}\n")

print(f"[OK] Résultats enregistrés dans {text_output}")

# --- Génération d'une image annotée ---
image = Image.open(image_path).convert('RGB')
draw = ImageDraw.Draw(image)
font_path = r"C:\Windows\Fonts\arial.ttf"

# --- Définir la police ---
font = ImageFont.truetype(font_path, 12)  # Ajuste la taille de la police

# --- Dessine les cadres verts et les numéros ---
idx = 1
for region in result:
    for line in region:
        box = line[0]
        points = [(int(x), int(y)) for x, y in box]
        draw.line(points + [points[0]], fill=(0, 255, 0), width=2)
        x_left = min(p[0] for p in points) - 10
        y_top = min(p[1] for p in points)
        draw.text((x_left, y_top), str(idx), fill=(0, 128, 0), font=font)
        idx += 1

# --- Sauvegarde HD ---
annotated_path = os.path.join(output_dir, "cadre-1_annotated_HD.png")
image.save(annotated_path, format="PNG", dpi=(300, 300))
print(f"[OK] Image annotée HD enregistrée dans {annotated_path}")
