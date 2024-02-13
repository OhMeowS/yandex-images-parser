from utils import save_images
from yandex_images_parser import Parser

parser = Parser()

Word = input("Введите запрос: ")
Ammount = int(input("Введите количество картинок: "))

#size - small, medium, large
square_cat = parser.query_search(query=Word,
                                 limit=Ammount,
                                 size=parser.size.medium,
                                 orientation=parser.orientation.square)

square_cat_url = square_cat[0]

# Ищем подобные картинки:
#similar_cats = parser.image_search(url=square_cat_url,
#                                   limit=1)
#print(similar_cats)

# Вывод результата:
#print(f"Cat:\n{square_cat_url}\n")

#print("Similar cats:")
#for cat in similar_cats:
    #print(cat)

# Сохраняем картинки:
output_dir = f"./images/{Word}"

save_images(square_cat, dir_path=output_dir, prefix="original_")  # Add prefix to filenames
#save_images(similar_cats, dir_path=output_dir, prefix="similar_", number_images=True)  # Add prefix and numbering
