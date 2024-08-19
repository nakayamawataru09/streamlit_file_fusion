import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
import io

# アプリのタイトル
st.title('PDFとPNGファイルの結合アプリ')

# ファイルアップロード機能
uploaded_files = st.file_uploader("PDFとPNGファイルをアップロードしてください", type=["pdf", "png"], accept_multiple_files=True)

pdf_files = []
png_files = []

if uploaded_files:
    # アップロードされたファイルを分類
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            pdf_files.append(uploaded_file)
        elif uploaded_file.type == "image/png":
            png_files.append(uploaded_file)

    if pdf_files and png_files:
        # 新しいPDFドキュメントを作成
        output_pdf = fitz.open()

        # PDFファイルを結合
        for pdf_file in pdf_files:
            pdf_doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            output_pdf.insert_pdf(pdf_doc)
            pdf_doc.close()

        # PNGファイルをPDFに変換して追加
        for png_file in png_files:
            image = Image.open(png_file)
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
        st.warning("PDFファイルとPNGファイルの両方をアップロードしてください。")

