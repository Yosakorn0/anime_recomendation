import matplotlib.pyplot as plt
import pandas            as pd
import cv2

anime_df = pd.read_csv('./dataset.csv')


def open_img(name_):
    url = './poster/' + name_.strip() \
                             .replace(" ", "_") \
                             .replace(":", "") \
                             .lower() + '.jpg'
    image = cv2.imread(url)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.title(name_)
    plt.imshow(img)
    plt.show()


# Output type
while True:
    s = str(input("Search / Top 5: ")).lower().replace(" ", "")
    if (s == "top5") | (s == "search"):
        break
    print("Please enter a valid value")

if s == 'top5':
    # Sorted anime by rating and print the top five highest rating
    sorted_anime_df = anime_df.sort_values(by='Rating',
                                           ascending=False)
    top_anime_df    = sorted_anime_df.head(5)

    for title, rating in zip(top_anime_df['Name'],
                             top_anime_df['Rating']):
        print(f"{title} - {rating}")
        open_img(title)

elif s == "search":
    # Take user input for anime description, genre 1, genre 2, aired status, and finish status
    a = str(input("Enter description: ")).lower()
    b = str(input("Enter genre 1: ")).lower()
    c = str(input("Enter genre 2: ")).lower()

    while True:
        try:
            d = str(input("Aired (Yes/No): ")).lower()
            if (d == 'yes') | (d == 'no'):
                break
            print("Please enter a valid value")
        except ValueError:
            print("Please enter a valid value")

    while True:
        try:
            e = str(input("Statust (Ongoing/End): ")).lower()
            if (e == 'ongoing') | (e == 'end'):
                break
            print("Please enter a valid value")
        except ValueError:
            print("Please enter a valid value")

    # Filter the anime dataframe based on the user input for description
    anime_des = anime_df.loc[anime_df['Description'].str.contains(a, case=False)]

    # If a genre 2 is provided, filter further based on genre 1 and 2, otherwise filter based on genre 1 only
    if c:
        anime_T1 = anime_des.loc[(anime_des['Type1'].astype(str).str.contains(b, case=False)) | \
                                 (anime_des['Type1'].astype(str).str.contains(c, case=False))]
        anime_T2 = anime_T1.loc[(anime_T1['Type2'].astype(str).str.contains(c, case=False)) | \
                                (anime_T1['Type2'].astype(str).str.contains(b, case=False))]
    else:
        anime_T2 = anime_des.loc[(anime_des['Type1'].astype(str).str.contains(b, case=False)) | \
                                 (anime_des['Type2'].astype(str).str.contains(b, case=False))]

    # Sort the resulting dataframe based on rating in descending order, and take the top 100 entries
    anime_sort_rating   = anime_T2.sort_values(by='Rating',
                                               ascending=False)
    anime_rating        = anime_sort_rating.head(120)

    # Filter the top 100 entries based on the user input for aired and finish status
    anime_air    = anime_rating.loc[anime_rating['Aired'].str.contains(d, case=False)]
    anime_finish = anime_air.loc[anime_air['Finished'].str.contains(e, case=False)]
    anime_finish = anime_finish.reset_index(drop=True)
    anime_finish.index += 1

    anime_finish['Name'] = anime_finish['Name'].astype('str')
    # Print the resulting dataframe
    print(anime_finish)

    file_names = anime_finish['Name']
    i = 1

    for name in file_names:
        open_img(name)
        i += 1
