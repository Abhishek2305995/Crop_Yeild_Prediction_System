"""Generate project documentation PDF"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, Image, HRFlowable)
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT, TA_RIGHT
import os

OUTPUT = '/mnt/user-data/outputs/Crop_Yield_Prediction_Documentation.pdf'
OUTPUTS_DIR = '/home/claude/crop-yield-prediction/outputs'

W, H = A4
MARGIN = 2 * cm

GREEN_DARK  = colors.HexColor('#1b4332')
GREEN_MID   = colors.HexColor('#2d6a4f')
GREEN_LIGHT = colors.HexColor('#52b788')
GREEN_BG    = colors.HexColor('#d8f3dc')
AMBER       = colors.HexColor('#e9c46a')
GRAY        = colors.HexColor('#6c757d')
LIGHT_GRAY  = colors.HexColor('#f8f9fa')
WHITE       = colors.white
BLACK       = colors.black

def make_styles():
    base = getSampleStyleSheet()

    heading1 = ParagraphStyle('H1', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=15, textColor=GREEN_DARK,
        spaceAfter=10, spaceBefore=16, leading=20)

    heading2 = ParagraphStyle('H2', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=14, textColor=GREEN_MID,
        spaceAfter=8, spaceBefore=12, leading=18)

    body = ParagraphStyle('Body', parent=base['Normal'],
        fontName='Helvetica', fontSize=12, textColor=BLACK,
        alignment=TA_JUSTIFY, spaceAfter=8, leading=18)

    bullet = ParagraphStyle('Bullet', parent=base['Normal'],
        fontName='Helvetica', fontSize=12, textColor=BLACK,
        spaceAfter=4, leading=16, leftIndent=16,
        bulletIndent=4, bulletFontName='Helvetica')

    center = ParagraphStyle('Center', parent=base['Normal'],
        fontName='Helvetica', fontSize=12, alignment=TA_CENTER,
        spaceAfter=6, leading=16)

    small = ParagraphStyle('Small', parent=base['Normal'],
        fontName='Helvetica', fontSize=10, textColor=GRAY,
        alignment=TA_JUSTIFY, spaceAfter=4, leading=14)

    title_main = ParagraphStyle('TitleMain', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=22, textColor=WHITE,
        alignment=TA_CENTER, spaceAfter=8, leading=28)

    title_sub = ParagraphStyle('TitleSub', parent=base['Normal'],
        fontName='Helvetica', fontSize=14, textColor=GREEN_BG,
        alignment=TA_CENTER, spaceAfter=6, leading=20)

    title_info = ParagraphStyle('TitleInfo', parent=base['Normal'],
        fontName='Helvetica-Bold', fontSize=13, textColor=WHITE,
        alignment=TA_CENTER, spaceAfter=4, leading=18)

    return dict(h1=heading1, h2=heading2, body=body, bullet=bullet,
                center=center, small=small, title_main=title_main,
                title_sub=title_sub, title_info=title_info)


def page_template(canvas, doc):
    """Draw page number at bottom-right on every page."""
    canvas.saveState()
    canvas.setFont('Helvetica', 10)
    canvas.setFillColor(GRAY)
    canvas.drawRightString(W - MARGIN, 1.2 * cm, str(doc.page))
    # Green footer line
    canvas.setStrokeColor(GREEN_LIGHT)
    canvas.setLineWidth(0.5)
    canvas.line(MARGIN, 1.6 * cm, W - MARGIN, 1.6 * cm)
    canvas.restoreState()


def build_pdf():
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
                            leftMargin=MARGIN, rightMargin=MARGIN,
                            topMargin=MARGIN, bottomMargin=2.5*cm)
    S = make_styles()
    story = []

    # ── PAGE 1: TITLE PAGE ──────────────────────────────────────────────────
    # Green banner table
    banner_data = [[
        Paragraph('CROP YIELD PREDICTION SYSTEM', S['title_main']),
    ]]
    banner = Table(banner_data, colWidths=[W - 2*MARGIN])
    banner.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GREEN_DARK),
        ('ROUNDEDCORNERS', [12, 12, 12, 12]),
        ('TOPPADDING', (0,0), (-1,-1), 28),
        ('BOTTOMPADDING', (0,0), (-1,-1), 28),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING', (0,0), (-1,-1), 20),
    ]))
    story.append(Spacer(1, 1.5*cm))
    story.append(banner)
    story.append(Spacer(1, 0.8*cm))

    story.append(Paragraph('An End-to-End Machine Learning Solution for Agriculture', S['center']))
    story.append(Paragraph('Data Engineering Project | April 2026', S['center']))
    story.append(Spacer(1, 1.2*cm))

    # Details table
    details = [
        ['Name', '[Your Full Name]'],
        ['Roll Number', '[Your Roll Number]'],
        ['Batch / Program', 'Data Engineering'],
        ['Submission Date', 'April 2026'],
        ['Institution', '[Your Institution Name]'],
    ]
    dt = Table(details, colWidths=[5*cm, W - 2*MARGIN - 5*cm])
    dt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), GREEN_MID),
        ('TEXTCOLOR', (0,0), (0,-1), WHITE),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 12),
        ('FONTNAME', (1,0), (1,-1), 'Helvetica'),
        ('BACKGROUND', (1,0), (1,-1), LIGHT_GRAY),
        ('ROWBACKGROUNDS', (1,0), (1,-1), [LIGHT_GRAY, WHITE]),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_LIGHT),
        ('PADDING', (0,0), (-1,-1), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(dt)
    story.append(Spacer(1, 2*cm))

    # Stats row
    stats = [['R² = 0.9848', '2000+ Records', '8 Crops', '3 ML Models'],
             ['Best Accuracy', 'Training Data', 'Supported', 'Compared']]
    st_t = Table(stats, colWidths=[(W - 2*MARGIN)/4]*4)
    st_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 14),
        ('BACKGROUND', (0,1), (-1,1), GREEN_BG),
        ('TEXTCOLOR', (0,1), (-1,1), GREEN_DARK),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,1), 10),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, WHITE),
    ]))
    story.append(st_t)
    story.append(PageBreak())

    # ── PAGE 2: PROBLEM STATEMENT + SOLUTION ────────────────────────────────
    story.append(Paragraph('1. Problem Statement', S['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN_LIGHT, spaceAfter=10))
    story.append(Paragraph(
        'Agriculture is the backbone of the Indian economy, employing over 50% of the workforce. '
        'However, traditional farming decisions depend heavily on empirical knowledge, local experience, '
        'and outdated methods, leading to inconsistent and suboptimal crop yields. Farmers face challenges '
        'such as unpredictable weather patterns, soil degradation, and poor resource allocation without '
        'data-driven guidance.',
        S['body']
    ))
    story.append(Paragraph(
        'The <b>Crop Yield Prediction System</b> addresses this challenge by building a Machine Learning '
        'pipeline that predicts crop yield (measured in tons per hectare) based on key agricultural inputs '
        'including climate data (rainfall, temperature, humidity), soil characteristics, crop type, region, '
        'and farming practices (fertilizer and pesticide usage). The system enables precision agriculture '
        'through accurate, explainable predictions.',
        S['body']
    ))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('2. Solution & Features', S['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN_LIGHT, spaceAfter=10))

    story.append(Paragraph('2.1 System Overview', S['h2']))
    story.append(Paragraph(
        'The system follows a complete data engineering pipeline: data ingestion from CSV sources, '
        'cleaning and feature engineering, model training with multiple algorithms, model serialization, '
        'REST API deployment, and a fully interactive Streamlit dashboard for end-users.',
        S['body']
    ))

    story.append(Paragraph('2.2 Key Features', S['h2']))
    features = [
        'Multi-crop support: Rice, Wheat, Maize, Soybean, Cotton, Sugarcane, Potato, Tomato',
        'Region-wise prediction across 5 agricultural zones (North, South, East, West, Central)',
        'Feature engineering: 14 features including composite indices (Temp x Rainfall, Fert/Area)',
        'Three ML models trained and compared: Gradient Boosting, Random Forest, Linear Regression',
        'Best model achieves R² = 0.9848 and RMSE = 2.78 (Gradient Boosting)',
        'Flask REST API with JSON input/output and input validation',
        'Streamlit interactive dashboard with real-time prediction and visualization',
        'SQLite database for full prediction history logging',
        'Joblib model serialization for fast inference',
        'Exploratory Data Analysis with 4 publication-quality charts',
    ]
    for f in features:
        story.append(Paragraph(f'• {f}', S['bullet']))

    story.append(PageBreak())

    # ── PAGE 3: TECH STACK + SCREENSHOTS ────────────────────────────────────
    story.append(Paragraph('3. Tech Stack', S['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN_LIGHT, spaceAfter=10))

    tech_data = [
        ['Layer', 'Technology', 'Purpose'],
        ['Language', 'Python 3.10+', 'Core programming language'],
        ['Data Processing', 'Pandas, NumPy', 'ETL, feature engineering, analysis'],
        ['Machine Learning', 'Scikit-learn', 'Model training & evaluation'],
        ['Visualization', 'Matplotlib, Seaborn', 'Charts, EDA plots, model plots'],
        ['API Framework', 'Flask 3.0', 'REST API for predictions'],
        ['Dashboard', 'Streamlit 1.37', 'Interactive web UI'],
        ['Storage', 'SQLite, Joblib', 'Prediction history, model serialization'],
        ['Version Control', 'Git + GitHub', 'Code hosting and collaboration'],
    ]
    tech_table = Table(tech_data, colWidths=[4.5*cm, 4.5*cm, W - 2*MARGIN - 9*cm])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_LIGHT),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,1), (0,-1), GREEN_BG),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0,1), (0,-1), GREEN_DARK),
    ]))
    story.append(tech_table)

    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph('4. Model Results & Visualizations', S['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN_LIGHT, spaceAfter=10))

    # Model comparison table
    story.append(Paragraph('4.1 Model Performance Comparison', S['h2']))
    model_data = [
        ['Model', 'RMSE', 'MAE', 'R² Score', 'Status'],
        ['Gradient Boosting', '2.7818', '1.4458', '0.9848', 'BEST'],
        ['Random Forest', '3.3835', '1.7677', '0.9775', 'Good'],
        ['Linear Regression', '21.5910', '15.5904', '0.0827', 'Baseline'],
    ]
    mt = Table(model_data, colWidths=[(W - 2*MARGIN)/5]*5)
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 11),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('ALIGN', (1,0), (-1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_LIGHT),
        ('PADDING', (0,0), (-1,-1), 8),
        # Highlight best model row
        ('BACKGROUND', (0,1), (-1,1), GREEN_BG),
        ('FONTNAME', (0,1), (-1,1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (-1,1), (-1,1), GREEN_DARK),
    ]))
    story.append(mt)

    story.append(Spacer(1, 0.6*cm))
    story.append(Paragraph('4.2 EDA Visualizations', S['h2']))
    eda_path = os.path.join(OUTPUTS_DIR, 'eda_plots.png')
    if os.path.exists(eda_path):
        img = Image(eda_path, width=W - 2*MARGIN, height=9*cm)
        story.append(img)
    story.append(Paragraph(
        'Figure 1: Exploratory Data Analysis — showing average yield by crop type, '
        'rainfall vs yield scatter, regional yield comparison, and feature correlation heatmap.',
        S['small']
    ))

    story.append(PageBreak())

    # ── PAGE 4: MORE CHARTS + UNIQUE POINTS ─────────────────────────────────
    story.append(Paragraph('4.3 Feature Importance & Model Accuracy', S['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN_LIGHT, spaceAfter=10))

    col_w = (W - 2*MARGIN - 0.5*cm) / 2
    fi_path = os.path.join(OUTPUTS_DIR, 'feature_importance.png')
    avp_path = os.path.join(OUTPUTS_DIR, 'actual_vs_predicted.png')
    cmp_path = os.path.join(OUTPUTS_DIR, 'model_comparison.png')

    if os.path.exists(fi_path) and os.path.exists(avp_path):
        imgs = [[Image(fi_path, width=col_w, height=7*cm),
                 Image(avp_path, width=col_w, height=7*cm)]]
        it = Table(imgs, colWidths=[col_w, col_w])
        story.append(it)
        story.append(Paragraph(
            'Figure 2 (left): Feature importance ranking from Gradient Boosting — Rainfall, Crop Type, '
            'and Fertilizer are the dominant predictors. Figure 3 (right): Actual vs Predicted scatter plot '
            'showing tight clustering around the ideal line (R² = 0.9848).',
            S['small']
        ))
        story.append(Spacer(1, 0.5*cm))

    if os.path.exists(cmp_path):
        story.append(Image(cmp_path, width=W - 2*MARGIN, height=6*cm))
        story.append(Paragraph(
            'Figure 4: Model comparison across RMSE, MAE, and R² metrics — Gradient Boosting '
            'significantly outperforms Linear Regression and edges ahead of Random Forest.',
            S['small']
        ))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph('5. Unique Points', S['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN_LIGHT, spaceAfter=10))

    unique = [
        '<b>Engineered composite features:</b> Temp_Rainfall_Index, Fert_per_Area, and Humidity_Rain '
        'capture non-linear interactions between variables that improve model accuracy.',
        '<b>Three-model comparison framework:</b> Systematic evaluation of Gradient Boosting, '
        'Random Forest, and Linear Regression with RMSE, MAE, and R² metrics.',
        '<b>Full prediction logging:</b> Every prediction is stored in a SQLite database with '
        'timestamp, inputs, and output for auditing and retraining.',
        '<b>Production-ready REST API:</b> Flask API with JSON validation, error handling, '
        'and structured responses — ready for integration with third-party applications.',
        '<b>Interactive dashboard:</b> Streamlit dashboard with tabbed layout — prediction form, '
        'model insights, history viewer, and project documentation in one interface.',
        '<b>Gradient Boosting superiority:</b> The GB model achieves 98.48% variance explanation, '
        'significantly outperforming baseline Linear Regression (8.27%).',
    ]
    for u in unique:
        story.append(Paragraph(f'• {u}', S['bullet']))

    story.append(PageBreak())

    # ── PAGE 5: FUTURE IMPROVEMENTS + PROJECT STRUCTURE ─────────────────────
    story.append(Paragraph('6. Future Improvements', S['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN_LIGHT, spaceAfter=10))

    future = [
        '<b>Real-time weather API integration:</b> Replace static inputs with live data from '
        'OpenWeatherMap or IMD API for dynamic, location-aware predictions.',
        '<b>Satellite imagery features:</b> Integrate NDVI (Normalized Difference Vegetation Index) '
        'from Sentinel-2 satellite data to capture crop health signals.',
        '<b>Time-series forecasting:</b> Implement LSTM or Prophet models for multi-season and '
        'multi-year yield forecasting beyond single-point prediction.',
        '<b>Cloud deployment:</b> Containerize with Docker and deploy on AWS EC2 or GCP Cloud Run '
        'with a managed database (RDS/Cloud SQL) for scalable production use.',
        '<b>Mobile application:</b> Build a React Native or Flutter app with offline capability '
        'for use by farmers with limited connectivity.',
        '<b>Hyperparameter optimization:</b> Implement Optuna or GridSearchCV for automated '
        'tuning to push model performance further.',
        '<b>Multi-language support:</b> Add Hindi and regional language support in the dashboard '
        'for accessibility in rural areas.',
        '<b>Anomaly detection:</b> Add data quality checks and outlier detection in the ingestion '
        'pipeline to flag suspicious sensor or user inputs.',
    ]
    for f in future:
        story.append(Paragraph(f'• {f}', S['bullet']))

    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph('7. Project File Structure', S['h1']))
    story.append(HRFlowable(width='100%', thickness=1, color=GREEN_LIGHT, spaceAfter=10))

    struct_data = [
        ['Path', 'Description'],
        ['data/crop_yield.csv', 'Main dataset (2000 records, 12 features)'],
        ['data/predictions.db', 'SQLite database logging all predictions'],
        ['src/preprocess.py', 'Data cleaning, encoding, scaling, train-test split'],
        ['src/train.py', 'Model training, evaluation, chart generation'],
        ['src/predict.py', 'Inference pipeline + DB logging'],
        ['model/best_model.joblib', 'Serialized Gradient Boosting model'],
        ['model/encoders.joblib', 'Fitted LabelEncoders for categoricals'],
        ['model/scaler.joblib', 'Fitted StandardScaler for numerics'],
        ['app/app.py', 'Flask REST API (POST /predict, GET /history)'],
        ['app/dashboard.py', 'Streamlit 4-tab interactive dashboard'],
        ['outputs/', 'EDA, feature importance, model comparison plots'],
        ['requirements.txt', 'Python dependency list'],
        ['README.md', 'Setup instructions and API documentation'],
    ]
    st_table = Table(struct_data, colWidths=[6*cm, W - 2*MARGIN - 6*cm])
    st_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('TEXTCOLOR', (0,0), (-1,0), WHITE),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTNAME', (0,1), (0,-1), 'Helvetica-Oblique'),
        ('TEXTCOLOR', (0,1), (0,-1), GREEN_MID),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, LIGHT_GRAY]),
        ('GRID', (0,0), (-1,-1), 0.3, GREEN_LIGHT),
        ('PADDING', (0,0), (-1,-1), 7),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(st_table)

    story.append(Spacer(1, 0.8*cm))
    # Footer note
    footer_data = [[
        Paragraph(
            'This project was developed as part of the Data Engineering curriculum. '
            'All code is original. The ML pipeline achieves R² = 0.9848 on the test set, '
            'demonstrating strong predictive accuracy for agricultural yield estimation.',
            ParagraphStyle('Footer', fontName='Helvetica', fontSize=11,
                           textColor=WHITE, alignment=TA_CENTER, leading=16)
        )
    ]]
    footer_table = Table(footer_data, colWidths=[W - 2*MARGIN])
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), GREEN_DARK),
        ('PADDING', (0,0), (-1,-1), 14),
        ('ROUNDEDCORNERS', [8, 8, 8, 8]),
    ]))
    story.append(footer_table)

    doc.build(story, onFirstPage=page_template, onLaterPages=page_template)
    print(f"PDF saved: {OUTPUT}")


if __name__ == '__main__':
    build_pdf()
