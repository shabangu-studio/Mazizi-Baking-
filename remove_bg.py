from PIL import Image
import os

def make_transparent(path, tol=30, backup=True):
    img = Image.open(path).convert('RGBA')
    datas = img.getdata()
    # sample top-left pixel as background
    bg = img.getpixel((0,0))[:3]
    newData = []
    for item in datas:
        r,g,b,a = item
        dist = ((r-bg[0])**2 + (g-bg[1])**2 + (b-bg[2])**2)**0.5
        if dist <= tol:
            newData.append((r,g,b,0))
        else:
            newData.append((r,g,b,a))
    img.putdata(newData)
    dirn = os.path.dirname(path)
    base = os.path.splitext(os.path.basename(path))[0]
    backup_path = os.path.join(dirn, base + '_backup.png')
    out_path = path
    if backup and not os.path.exists(backup_path):
        img_orig = Image.open(path).convert('RGBA')
        img_orig.save(backup_path)
        print(f'Backup saved to {backup_path}')
    img.save(out_path)
    print(f'Saved transparent image to {out_path}')

if __name__ == '__main__':
    repo_root = os.path.dirname(__file__)
    logo_path = os.path.join(repo_root, 'Logo.png')
    if not os.path.exists(logo_path):
        print('Logo.png not found in', repo_root)
    else:
        make_transparent(logo_path, tol=40)
