from app.config.logging_config import get_logger
from app.exceptions.classification_exception import ClassificationException
from app.util.iptc.news_classifier import NewsClassifier

logger = get_logger(class_name=__name__)

classifier = NewsClassifier().load("app/util/iptc/artifacts/models/iptc_news_classifier.zip")


class ClassificationService:

    @classmethod
    def get_classification(cls, text, category_count):
        try:
            logger.info("Classification Process Started")
            prediction = classifier.classify_article(data=text, category_count=category_count)
            logger.info("Classification Process End")
            return prediction
        except Exception as ex:
            logger.error(f"Classification Process Error: {str(ex)}")
            logger.info("Classification Process End with Error")
            raise ClassificationException(str(ex), str(ex))

