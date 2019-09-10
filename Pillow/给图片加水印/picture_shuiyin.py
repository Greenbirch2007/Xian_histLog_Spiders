from PIL import Image
#创建底图
target = Image.new('RGBA', (800, 800), (0, 0, 0, 0))
#打开头像
nike_image = Image.open("/home/w/timg.jpeg")
nike_image = nike_image.resize((800, 800))
#打开装饰
hnu_image = Image.open("/home/w/DVlogo.png")
# 分离透明通道
r,g,b,a = hnu_image.split()
# 将头像贴到底图
nike_image.convert("RGBA")
target.paste(nike_image, (0,0))

#将装饰贴到底图
hnu_image.convert("RGBA")
target.paste(hnu_image,(0,0), mask=a)

# 保存图片
target.save("/home/w/f.png")