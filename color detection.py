import cv2
import pandas as pd

# Load image safely
img_path ="D:\GK NM\Plain_Landscape.jpg"    # <-- update if needed
img = cv2.imread(img_path)

if img is None:
    print("⚠ Image not found! Check file path.")
    exit()

# Load colors CSV
csv_path = r"D:\GK NM\Colors.csv"
cols = ["color", "color_name", "hex", "R", "G", "B"]
df = pd.read_csv(csv_path, names=cols, header=None)

# Click to detect color
clicked = False
r = g = b = xpos = ypos = 0

def getColorName(R, G, B):
    minimum = 10000
    cname = ""
    for i in range(len(df)):
        d = abs(R - int(df.loc[i, "R"])) + abs(G - int(df.loc[i, "G"])) + abs(B - int(df.loc[i, "B"]))
        if d < minimum:
            minimum = d
            cname = df.loc[i, "color_name"]
    return cname

def draw_function(event, x, y, flags, param):
    global b, g, r, xpos, ypos, clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked = True
        xpos = x
        ypos = y
        b, g, r = img[y, x]
        b, g, r = int(b), int(g), int(r)

cv2.namedWindow("Color Detection")
cv2.setMouseCallback("Color Detection", draw_function)

while True:
    cv2.imshow("Color Detection", img)
    if clicked:
        cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)
        text = f"{getColorName(r, g, b)} R={r} G={g} B={b}"
        cv2.putText(img, text, (50, 50), 2, 0.8,
                    (255, 255, 255) if r + g + b < 600 else (0, 0, 0), 2)
        clicked = False
    if cv2.waitKey(20) & 0xFF == 27:  # press Esc to exit
        break

cv2.destroyAllWindows()
