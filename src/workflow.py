import luigi


class DownloadTask(luigi.Task):

    # date hour parameter
    date_hour = luigi.DateHourParameter()

    @property
    def url(self) -> str:


    def run(self):
        pass

    def output(self):
        pass
