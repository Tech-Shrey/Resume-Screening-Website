# Step 9 : important libraries

import streamlit as st   # USE FOR A WEBSITE
import pickle
import re
import nltk
nltk.download("punkt")
nltk.download("stopwords")

# STEP 10: LOADING MODELS KNeighborsClassifier AND tfidf , label_encoder
KNeighborsClassifier = pickle.load(open("KNeighborsClassifier.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder_mapping.pkl", "rb"))


# Step 11 : Clean the unseen resume
def clean_resume(txt):
    cleantxt = re.sub(r"http\S+\s"," ", txt)
    cleantxt = re.sub(r"#\S+\s"," ", cleantxt)
    cleantxt = re.sub(r"@\S+"," ", cleantxt)
    cleantxt = re.sub(r"[%s]" % re.escape(r"""!@#$%^&*()_-=+~`/*-.?>,<'";:|[\]{}"""), " ", cleantxt)
    cleantxt = re.sub(r"[^\x00-\x7f]", " ", cleantxt)
    cleantxt = re.sub(r"\s+", " ", cleantxt)  # whitespace handling
    return cleantxt


# Step 12 : WEBSITE FUNCTION
def main():
    st.title("Resume Screening Website")
    upload_file = st.file_uploader("Upload Resume", type=["txt", "pdf", "doc"])

    if upload_file is not None:
        resume_byte = upload_file.read()
        try:
            resume_text = resume_byte.decode("utf-8")
        except UnicodeDecodeError:
            resume_text = resume_byte.decode("latin-1")  # If utf-8 decoding fails, trying decoding with "latin-1"

        cleaned_resume = clean_resume(resume_text)
        cleaned_resume = tfidf.transform([cleaned_resume])  # we put resume text in array bracket b/c the function actually work on 1D array as compare to dataframe in jupyter
        prediction_id = KNeighborsClassifier.predict(cleaned_resume)[0]  # we put [0] b/c we need categorise no. which was at zero index in dataframe
        st.write(prediction_id)  # we use st.write to print something on a website rather than use of print function

        category_name = label_encoder.inverse_transform([prediction_id])[0]
        st.write("Predicted Category:", category_name)


# Step 13 : python main
if __name__ == "__main__":
    main()


# streamlit run app.py