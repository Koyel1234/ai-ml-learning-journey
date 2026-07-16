from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime

# Create PDF
pdf_file = "ai-ml-curriculum.pdf"
doc = SimpleDocTemplate(pdf_file, pagesize=letter)
elements = []

# Styles
styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontSize=24,
    textColor=colors.HexColor('#1f4788'),
    spaceAfter=30,
    alignment=1
)

heading_style = ParagraphStyle(
    'CustomHeading',
    parent=styles['Heading2'],
    fontSize=14,
    textColor=colors.HexColor('#2e5c8a'),
    spaceAfter=12,
    spaceBefore=12
)

# Title
title = Paragraph("AI & Machine Learning Curriculum", title_style)
elements.append(title)
elements.append(Spacer(1, 0.2*inch))

# Subtitle with date
subtitle = Paragraph(f"<b>Deep Learning & GenAI Specialization</b><br/>Updated: {datetime.now().strftime('%B %d, %Y')}", styles['Normal'])
elements.append(subtitle)
elements.append(Spacer(1, 0.3*inch))

# Course Structure
elements.append(Paragraph("Course Structure", heading_style))

# Create table data
table_data = [
    ['Module', 'Topic', 'Duration', 'Level'],
    ['1', 'Python Fundamentals', '2 weeks', 'Beginner'],
    ['2', 'NumPy & Pandas', '2 weeks', 'Beginner'],
    ['3', 'Data Visualization', '1 week', 'Beginner'],
    ['4', 'Statistics & Probability', '2 weeks', 'Intermediate'],
    ['5', 'Machine Learning Basics', '3 weeks', 'Intermediate'],
    ['6', 'Supervised Learning', '3 weeks', 'Intermediate'],
    ['7', 'Unsupervised Learning', '2 weeks', 'Intermediate'],
    ['8', 'Neural Networks', '4 weeks', 'Advanced'],
    ['9', 'Deep Learning', '4 weeks', 'Advanced'],
    ['10', 'Computer Vision', '3 weeks', 'Advanced'],
    ['11', 'Natural Language Processing', '4 weeks', 'Advanced'],
    ['12', 'Generative AI & LLMs', '4 weeks', 'Advanced'],
    ['13', 'RAG & Prompt Engineering', '2 weeks', 'Advanced'],
    ['14', 'AI Applications & Deployment', '2 weeks', 'Advanced'],
]

table = Table(table_data, colWidths=[0.8*inch, 2.2*inch, 1.2*inch, 1.2*inch])
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2e5c8a')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 11),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ('GRID', (0, 0), (-1, -1), 1, colors.black)
]))

elements.append(table)
elements.append(Spacer(1, 0.3*inch))

# Page Break
elements.append(PageBreak())

# Learning Outcomes
elements.append(Paragraph("Learning Outcomes", heading_style))
outcomes = [
    "Master Python programming for data science and AI",
    "Understand machine learning algorithms and their applications",
    "Build and train deep learning models",
    "Work with state-of-the-art generative AI models",
    "Implement RAG systems and prompt engineering techniques",
    "Deploy AI models to production",
    "Handle real-world datasets and preprocessing",
    "Perform exploratory data analysis and visualization"
]

for outcome in outcomes:
    elements.append(Paragraph(f"• {outcome}", styles['Normal']))
    elements.append(Spacer(1, 0.1*inch))

elements.append(Spacer(1, 0.2*inch))

# Prerequisites
elements.append(Paragraph("Prerequisites", heading_style))
prerequisites = [
    "Basic understanding of mathematics (algebra, calculus)",
    "Familiarity with programming concepts (loops, functions, data structures)",
    "Basic knowledge of statistics",
    "Linux/Command line basics (helpful but not mandatory)"
]

for prereq in prerequisites:
    elements.append(Paragraph(f"• {prereq}", styles['Normal']))
    elements.append(Spacer(1, 0.1*inch))

elements.append(Spacer(1, 0.2*inch))

# Tools & Technologies
elements.append(Paragraph("Tools & Technologies", heading_style))
tools = [
    "Python 3.8+",
    "Jupyter Notebook & VS Code",
    "TensorFlow & PyTorch",
    "Scikit-learn",
    "Pandas & NumPy",
    "Matplotlib & Seaborn",
    "OpenAI API & Google Generative AI",
    "LangChain",
    "Docker & Git"
]

for tool in tools:
    elements.append(Paragraph(f"• {tool}", styles['Normal']))
    elements.append(Spacer(1, 0.1*inch))

# Build PDF
doc.build(elements)
print(f"PDF created successfully: {pdf_file}")
