import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

# アプリのタイトル
st.title('PDFと画像ファイルの結合アプリ')

# ファイルアップロード機能
uploaded_files = st.file_uploader("PDF、PNG、JPGファイルをアップロードしてください", type=["pdf", "png", "jpg"], accept_multiple_files=True)

pdf_files = []
image_files = []

if uploaded_files:
    # アップロードされたファイルを分類
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            pdf_files.append(uploaded_file)
        elif uploaded_file.type in ["image/png", "image/jpeg"]:
            image_files.append(uploaded_file)

    if pdf_files and image_files:
        # 新しいPDFドキュメントを作成
        output_pdf = fitz.open()

        # PDFファイルを結合
        for pdf_file in pdf_files:
            pdf_doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            output_pdf.insert_pdf(pdf_doc)
            pdf_doc.close()

        # 画像ファイルをPDFに変換して追加
        for image_file in image_files:
            image = Image.open(image_file)
            pdf_bytes = io.BytesIO()
            image.save(pdf_bytes, format="PDF")
            image_pdf = fitz.open("pdf", pdf_bytes.getvalue())
            output_pdf.insert_pdf(image_pdf)
            image_pdf.close()

        # 結合したPDFをバイトストリームとして保存
        output_stream = io.BytesIO()
        output_pdf.save(output_stream)
        output_pdf.close()

        # ダウンロード可能なPDFとして提供
        st.download_button(
            label="結合されたPDFをダウンロード",
            data=output_stream.getvalue(),
            file_name="merged_output.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("PDFファイルと画像ファイルの両方をアップロードしてください。")
