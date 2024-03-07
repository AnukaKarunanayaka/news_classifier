import spacy

from app.config.logging_config import get_logger
from app.exceptions.classification_exception import ClassificationException
from app.util.iptc.iptc_news_classifier import IptcNewsClassifier

logger = get_logger(class_name=__name__)

iptc_classifier = IptcNewsClassifier().load("app/util/iptc/artifacts/models/iptc_news_classifier.zip")
nlp = spacy.load("xx_ent_wiki_sm")

class ClassificationService:

    @classmethod
    def get_iptc_classification(cls, text):
        try:
            logger.info("IPTC Classification Process Started")
            prediction = iptc_classifier.classify_article(text=text, language='en')
            classification = []
            for predict in prediction:
                classification.append(predict['class'])
            logger.info("IPTC Classification Process End")
            return classification if len(classification) > 0 else ["Other"]
        except Exception as ex:
            logger.error(f"IPTC Classification Process Error: {str(ex)}")
            logger.info("IPTC Classification Process End with Error")
            raise ClassificationException(str(ex), str(ex))

