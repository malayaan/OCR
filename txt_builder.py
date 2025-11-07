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
                print(text, coords)  # Affiche le texte et les coordonnées pour vérification
    
    return data

# Fonction pour trier les données OCR par la coordonnée Y (verticale)
def sort_by_y(data):
    return sorted(data, key=lambda x: x["coords"][0][1])

# Fonction pour reconstruire le texte avec les coordonnées et ajouter des sauts de ligne et espaces
def reconstruct_text_with_layout(sorted_data):
    reconstructed_text = ""
    previous_y = None
    last_x = 0  # Pour gérer les espaces entre les éléments sur la même ligne
    
    for item in sorted_data:
        text = item["text"]
        
        # Vérifie que les coordonnées ont bien un élément avant de continuer
        if len(item["coords"]) > 1:
            current_y = item["coords"][0][1]
            current_x = item["coords"][0][0]
        else:
            continue  # Si la coordonnée est manquante, ignore cet élément
        
        # Si la différence entre les Y est importante, cela signifie un nouveau bloc de texte
        if previous_y and abs(current_y - previous_y) > 20:  # 20 est un seuil d'espacement à ajuster
            reconstructed_text += "\n"  # Ajouter un saut de ligne pour simuler une nouvelle ligne dans le document

        # Si le texte est à la même hauteur (Y), on gère les espacements horizontaux
        if previous_y and abs(current_y - previous_y) <= 20:
            # Vérifie si la coordonnée X est trop éloignée du dernier texte ajouté, alors ajoute un espace
            if current_x - last_x > 50:  # 50 est un seuil pour l'espacement entre les mots/colonnes
                reconstructed_text += "   "  # Ajoute plusieurs espaces
        reconstructed_text += text + " "
        
        # Met à jour la dernière position X pour l'espacement horizontal
        last_x = item["coords"][1][0] if len(item["coords"]) > 1 else current_x
        previous_y = current_y
    
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