from mkite_core.models import JobInfo, JobResults
from mkite_core.recipes.chain import JobPipe


class UpdateStructurePipe(JobPipe):
    """Updates the JobInfo to have the output structure of the previous job as an input"""
    def modify_info(self):
        structure = self.results.nodes[0].chemnode
        info = self.info.copy()
        info.inputs = [structure]
        return info
