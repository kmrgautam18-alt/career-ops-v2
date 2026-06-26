class JobNotFoundException(Exception):

    def __init__(self, job_id: int):
        self.job_id = job_id
        self.message = f"Job with id {job_id} not found."
        super().__init__(self.message)
