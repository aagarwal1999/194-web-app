from storage.models.production_data import ProductionData

class ProdOperations:

    def __init__(self, config):

        # load models 

    def postprocess_model_output(self, out_text):

        pass

    def preprocess_model_input(self, text):
        return

    def summarize(self, session, text):

        text = self.preprocess_model_input(text)
        # predict model 1
        # predict model 2

        one_line_summary = self.post_process_model_output(text)
        one_paragraph_summary = self.post_process_model_output(text)
        new_data_pont = ProductionData(data=data, time=time, one_line_summary=one_line_summary, one_paragraph_summary=one_paragraph_summary)
        session.add(new_data_pont)
        return one_line_summary, one_paragraph_summary

    def get_prod_metrics(self, session):
        pass

    def get_recent_prod_data(self, session):
        pass

    def get_daily_prod_data(self, session):
        pass

    def get_all_metrics(self, session):
        pass


