from PIL import Image, ImageDraw, ImageFont, ImageStat
from scrapper import download_thumb
import random


from PIL import Image

def collage(photo_path, template):
    """
    This function generates a collage image by combining a given photo with a template.
    The photo is resized and cropped/padded to fit the template dimensions.
    The collage is then saved as a JPEG file.

    Parameters:
    photo_path (str): The file path of the photo to be used in the collage.
    template (str): The name of the template image file (without the file extension).

    Returns:
    str: The file path of the generated collage image.
    """
    template = Image.open(f"assets/{template}.png").convert("RGBA")
    photo = Image.open(photo_path).convert("RGBA")

    # Resize to get a height of 720 pixels + maintain aspect ratio
    photo = photo.resize((int(photo.width * 720 / photo.height), 720), resample=Image.Resampling.LANCZOS)

    # If the resized photo's width is larger than the template, crop 
    if photo.width > template.width:
        left = (photo.width - template.width) // 2
        right = left + template.width
        photo = photo.crop((left, 0, right, 720))
    # If the resized photo's width is smaller than the template, pad
    elif photo.width < template.width:
        new_photo = Image.new("RGBA", (template.width, 720))
        left = (template.width - photo.width) // 2
        new_photo.paste(photo, (left, 0))
        photo = new_photo


    collage = Image.new("RGBA", (template.width, template.height))
    collage.paste(photo, (0, 0))
    collage.paste(template, (0, 0), mask=template)

    collage.convert("RGB").save('assets/images/collage.jpeg')
    #collage.show()

    return 'assets/images/collage.jpeg'



def add_text(fetch):

    choice_template = random.choices(['template1','template2'],weights=(70,30),k=1)[0]
    img = Image.open(collage(download_thumb(fetch[5]),choice_template))  # Open the image
    draw = ImageDraw.Draw(img)

    dico = {'template1':{'title_color':(215, 38, 56),},
            'template2':{'title_color':(38,33,97)},
    }

    # Initial font size and settings
    initial_font_size = 70
    bold_font = ImageFont.truetype('assets/ShurjoWeb_700_v5_1.ttf', initial_font_size)
    title = fetch[1] 
    title_color = dico[choice_template]['title_color']
    title_position = (150, 765)

    if fetch[4]:
        title_position = (150, 780)
        subtopic = fetch[4]
        subtopic_font = ImageFont.truetype('assets/ShurjoWeb_400_v5_1.ttf', 40)
        subtopic_color = (67,67,69)
        subtopic_pos = ((img.width - subtopic_font.getlength(subtopic)) / 2 ,715)
        draw.text(subtopic_pos,subtopic,subtopic_color,subtopic_font)

    regular_font = ImageFont.truetype('assets/ShurjoWeb_400_v5_1.ttf', 25)
    topic = fetch[3] + " | "
    topic_color = (0,0,0)
    topic_position = (50,1030)

    date = fetch[7]
    date_color = (102,102,102)
    date_position = (50+regular_font.getlength(topic),1030) # to calculate
    
    caption_font_size = 22
    caption_font = ImageFont.truetype('assets/ShurjoWeb_400_v5_1.ttf',caption_font_size )
    caption = fetch[-1]
    caption_position = (645,645)


    # Define maximum width and height for title
    max_width = img.width - title_position[0] - 120
    max_height = 160  # Maximum height for the text block

    # Function to split text into lines that fit within max_width
    def split_text_into_lines(text, font, max_width):
        lines = []
        words = text.split(' ')
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            test_line_width = font.getlength(test_line)
            if test_line_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        if current_line:
            lines.append(current_line.strip())
        return lines

    # Adjust font size to fit within max height
    lines = split_text_into_lines(title, bold_font, max_width)
    total_text_height = sum(bold_font.getbbox(line)[3] for line in lines)
    
    while total_text_height > max_height and initial_font_size > 50: 
        initial_font_size -= 1
        bold_font = ImageFont.truetype('assets/ShurjoWeb_700_v5_1.ttf', initial_font_size)
        lines = split_text_into_lines(title, bold_font, max_width)
        total_text_height = sum(bold_font.getbbox(line)[3] for line in lines)+10
    
    if len(lines) > 1 and bold_font.getlength(lines[-1]) <= 330 :
        lines[-2] += ' ' + lines[-1]
        lines = lines[:-1] 

        max_title_width = max(bold_font.getbbox(line)[2] for line in lines)
        while max_title_width > max_width and initial_font_size > 50:
            initial_font_size -= 1
            bold_font = ImageFont.truetype('assets/ShurjoWeb_700_v5_1.ttf', initial_font_size)
            max_title_width = max(bold_font.getbbox(line)[2] for line in lines)


    if len(lines)==1:
        title_position = (185,780)
    
    # Draw each line of text, center-aligned
    y = title_position[1]
    max_line_width = max([bold_font.getlength(line) for line in lines])
    for line in lines:
        line_width = bold_font.getlength(line)
        x = (max_line_width - line_width) / 2 + (img.width - max_line_width) / 2 # Center the text horizontally
        draw.text((x, y), line, font=bold_font, fill=title_color)
        y += bold_font.getbbox(line)[3]+10   # Move to the next line based on the font size
    
    # caption
    if caption:
        max_caption_width = 435
        caption_lines = split_text_into_lines(caption, caption_font, max_caption_width)
        
        if caption_font.getlength(caption_lines[-1]) <= 105 :
           caption_lines[-2] += ' ' + caption_lines[-1]
           caption_lines = caption_lines[:-1] 

           while caption_font.getlength(caption_lines[-1])>max_caption_width and caption_font_size>10:
               caption_font_size -= 1
               caption_font = ImageFont.truetype('assets/ShurjoWeb_400_v5_1.ttf',caption_font_size )
        
        

        total_caption_height = sum(caption_font.getbbox(line)[3] for line in caption_lines)
            
        # Adjust the caption position if it's less than 430px from the bottom
        bottom_y = caption_position[1] + total_caption_height
        while bottom_y > img.height - 435 and caption_position[1] > 0:
            caption_position = (caption_position[0], caption_position[1] - 1)
            bottom_y = caption_position[1] + total_caption_height

        # Change caption color based on it's background
        def calculate_average_brightness(image, bbox):
            cropped_image = image.crop(bbox)
            stat = ImageStat.Stat(cropped_image)
            r, g, b = stat.mean[:3]
            return (r + g + b) / 3

        caption_bbox = (caption_position[0], caption_position[1],
                        caption_position[0] + max_caption_width, caption_position[1] + total_caption_height)

        average_brightness = calculate_average_brightness(img, caption_bbox)
        brightness_threshold = 140 # favorising white ( 128 if default)

        if average_brightness > brightness_threshold:
            caption_color = (0, 0, 0) # Black
        else:
            caption_color = (255, 255, 255) # white


        # Draw the caption
        y = caption_position[1]
        for line in caption_lines:
            line_width = caption_font.getlength(line)
            x = caption_position[0] + (max_caption_width - line_width) # right aligned
            draw.text((x, y), line, font=caption_font, fill=caption_color)
            y += caption_font.getbbox(line)[3]

    draw.text(topic_position,topic,fill=topic_color,font=regular_font)
    draw.text(date_position, date, fill=date_color, font=regular_font)
    
    img.save('assets/images/inserted.jpeg')
