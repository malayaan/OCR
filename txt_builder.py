import re

# Fonction pour lire et extraire le texte et les coordonnées depuis le fichier OCR
def read_ocr_data(file_path):
    data = []
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Utilisation d'une expression régulière pour extraire le texte et les coordonnées
            match = re.match(r'Texte:\s*(.*?)\s*\(Confiance:.*?\)\s*- Coordonnées:\s*\((.*?)\)', line.strip())
            if match:
                text = match.group(1)
                coords_str = match.group(2)
                coords = [tuple(map(int, coord.split(','))) for coord in coords_str.split('), (')]
                data.append({'text': text, 'coords': coords})
    
    return data

# Fonction pour trier les données OCR par la coordonnée Y (verticale)
def sort_by_y(data):
    return sorted(data, key=lambda x: x["coords"][0][1])

# Fonction pour reconstruire le texte avec les coordonnées et ajouter des sauts de ligne et espaces
def reconstruct_text_with_layout(sorted_data):
    reconstructed_text = ""
    previous_y = None
    current_line = []
    line_threshold = 5  # Seuil pour la différence Y pour déterminer la ligne
    x_threshold = 50   # Seuil pour l'espacement en X entre les éléments
    
    # Parcours les données triées pour organiser le texte
    for item in sorted_data:
        text = item["text"]
        current_y = item["coords"][0][1]
        current_x = item["coords"][0][0]

        # Si la différence entre les Y est importante, cela signifie un nouveau bloc de texte (nouvelle ligne)
        if previous_y and abs(current_y - previous_y) > line_threshold:
            reconstructed_text += "\n"  # Ajouter un saut de ligne pour simuler une nouvelle ligne dans le document
            # Afficher la ligne courante avant de commencer une nouvelle ligne
            reconstructed_text += " ".join([i["text"] for i in sorted(current_line, key=lambda x: x["coords"][0][0])]) + "\n"
            current_line = []  # Réinitialiser la ligne courante
        
        # Ajouter le texte à la ligne courante, trié par X (coordonnée horizontale)
        current_line.append(item)

        # Mettre à jour la dernière position Y
        previous_y = current_y
    
    # Ajouter la dernière ligne après le tri par X
    if current_line:
        reconstructed_text += " ".join([i["text"] for i in sorted(current_line, key=lambda x: x["coords"][0][0])])  # Trier par X (gauche à droite)

    return reconstructed_text.strip()

# Chemin vers le fichier OCR
file_path = r"C:\Users\decroux paul\Documents\info\OCR\output\cadre-1.txt"

# Lire et traiter les données OCR
ocr_data = read_ocr_data(file_path)

# Trier les données OCR par coordonnée Y
sorted_data = sort_by_y(ocr_data)

# Reconstruire le texte avec mise en page et espacements
reconstructed_text = reconstruct_text_with_layout(sorted_data)

# Afficher le texte reconstruit
print(reconstructed_text)

# Sauvegarder le texte reconstruit dans un nouveau fichier
output_reconstructed_path = r"C:\Users\decroux paul\Documents\info\OCR\output\cadre-1_reconstructed.txt"
with open(output_reconstructed_path, "w", encoding="utf-8") as f:
    f.write(reconstructed_text)
