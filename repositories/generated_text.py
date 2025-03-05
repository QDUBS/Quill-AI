from models.generated_text import GeneratedText, db


class GeneratedTextRepository:
    @staticmethod
    def save_generated_text(user_id, prompt, response):
        new_text = GeneratedText(
            user_id=user_id, prompt=prompt, response=response)
        db.session.add(new_text)
        db.session.commit()
        return new_text

    @staticmethod
    def get_generated_text_by_id(text_id):
        return GeneratedText.query.get_or_404(text_id)

    @staticmethod
    def delete_generated_text(text):
        db.session.delete(text)
        db.session.commit()
