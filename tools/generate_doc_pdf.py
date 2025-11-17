from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image
import datetime
import os
from PIL import Image as PILImage, ImageDraw, ImageFont

output_path = r"c:\Users\khant\OneDrive\Desktop\Message\Message_Board_Documentation.pdf"

doc_title = "Message Board — Project Documentation"

# Short one-page doc (summary). Keep paragraphs concise so it fits one page.
content_sections = [
    ("Project title", "Message Board — Django-based simple message board with modern UI, authentication, and AJAX editing."),
    ("Short summary", "A lightweight Django application that lets users sign up, log in, create short text posts, edit and delete their own posts, and view posts from others. The UI uses Bootstrap 5 and Bootstrap Icons; create/edit/delete are enhanced with AJAX and Bootstrap modals for a smooth UX."),
    ("Key features", "Sign up and login; create/edit/delete posts with per-user permissions; paginated timeline; human-friendly timestamps; AJAX interactions (create/edit/delete); Bootstrap-based responsive UI; admin integration; unit tests for core flows."),
    ("Architecture & files", "Django (MVT) app with main components: 'posts' app containing models, views, forms, templates, static assets, and tests. Key files: manage.py, mb_project/settings.py, posts/models.py, posts/views.py, posts/forms.py, posts/urls.py, templates/, static/js/main.js, static/css/style.css." ) ,
    ("Local run & tests", "Create venv, install requirements, run migrations, create superuser, then runserver. Tests are executed via 'python manage.py test' and use a temporary test database to verify behavior without touching the development DB."),
    ("Notes & next steps", "For production: set a secure SECRET_KEY, DEBUG=False, proper ALLOWED_HOSTS, configure static files and HTTPS. Optional enhancements: avatar uploads, Markdown support, real-time updates with Channels, moderation tools.")
]

# Create PDF (enhanced single page layout)
styles = getSampleStyleSheet()
# register a nicer sans font if available (fallback handled by ReportLab)
try:
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
    base_font = 'DejaVuSans'
except Exception:
    base_font = styles['Normal'].fontName

styles.add(ParagraphStyle(name='TitleCenter', parent=styles['Title'], alignment=TA_CENTER, spaceAfter=6, fontName=base_font))
styles.add(ParagraphStyle(name='Heading', parent=styles['Heading2'], textColor=colors.HexColor('#0d6efd'), fontName=base_font))
styles.add(ParagraphStyle(name='Body', parent=styles['BodyText'], leading=12, fontName=base_font))
styles.add(ParagraphStyle(name='Small', parent=styles['BodyText'], leading=10, fontSize=9, fontName=base_font))

story = []
story.append(Paragraph(doc_title, styles['TitleCenter']))
story.append(Spacer(1, 4*mm))

# Produce a compact layout: render headings and body; render Key features as bullets
for heading, paragraph in content_sections:
    if heading == 'Key features':
        story.append(Paragraph(f"<b>{heading}</b>", styles['Heading']))
        story.append(Spacer(1, 1*mm))
        features = paragraph.split(';')
        list_items = [ListItem(Paragraph(item.strip(), styles['Body']), leftIndent=6) for item in features if item.strip()]
        story.append(ListFlowable(list_items, bulletType='bullet'))
        story.append(Spacer(1, 3*mm))
    else:
        story.append(Paragraph(f"<b>{heading}</b>", styles['Heading']))
        story.append(Spacer(1, 1*mm))
        story.append(Paragraph(paragraph, styles['Body']))
        story.append(Spacer(1, 3*mm))

# Optional screenshots: include up to two images from screenshots/ or generate placeholders
screenshots_dir = os.path.join(os.path.dirname(output_path), 'screenshots')
if os.path.isdir(screenshots_dir):
    imgs = [f for f in os.listdir(screenshots_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    for img_name in imgs[:2]:
        img_path = os.path.join(screenshots_dir, img_name)
        try:
            im = Image(img_path)
            im._restrictSize(80*mm, 60*mm)
            story.append(im)
            story.append(Spacer(1, 3*mm))
        except Exception as e:
            print(f"Could not include image {img_path}: {e}")
else:
    # create screenshots dir and placeholder images
    try:
        os.makedirs(screenshots_dir, exist_ok=True)
        for i in range(1, 3):
            ph_path = os.path.join(screenshots_dir, f'placeholder_{i}.png')
            img_w, img_h = (800, 480)
            img = PILImage.new('RGB', (img_w, img_h), color=(245, 247, 250))
            d = ImageDraw.Draw(img)
            d.rectangle([10, 10, img_w-10, img_h-10], outline=(200,200,200), width=2)
            try:
                fnt = ImageFont.truetype('DejaVuSans.ttf', 36)
            except Exception:
                fnt = ImageFont.load_default()
            txt = f'Screenshot {i}'
            tw, th = d.textsize(txt, font=fnt)
            d.text(((img_w-tw)/2, (img_h-th)/2), txt, font=fnt, fill=(120,120,120))
            img.save(ph_path)
            im = Image(ph_path)
            im._restrictSize(80*mm, 60*mm)
            story.append(im)
            story.append(Spacer(1, 3*mm))
    except Exception as e:
        print('Could not create placeholder images:', e)


def _header_footer(canvas, doc):
    canvas.saveState()
    w, h = A4
    # header bar
    canvas.setFillColor(colors.HexColor('#0d6efd'))
    canvas.rect(0, h - 36, w, 36, stroke=0, fill=1)
    canvas.setFillColor(colors.white)
    canvas.setFont(base_font, 14)
    canvas.drawString(18*mm, h - 26, doc_title)
    # footer
    footer_text = f'Generated: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    canvas.setFont(base_font, 8)
    canvas.setFillColor(colors.grey)
    canvas.drawRightString(w - 18*mm, 12*mm, footer_text)
    canvas.restoreState()

pdf = SimpleDocTemplate(output_path, pagesize=A4,
                        rightMargin=18*mm, leftMargin=18*mm, topMargin=28*mm, bottomMargin=18*mm)
pdf.build(story, onFirstPage=_header_footer, onLaterPages=_header_footer)
print(f"Wrote PDF to: {output_path}")
