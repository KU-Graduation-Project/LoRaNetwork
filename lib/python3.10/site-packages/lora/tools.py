from collections import Counter


def get_num_jobs_per_host(lora_session):
    jobs = lora_session.getAllJobDetails()['output']['jobs']
    hosts = [j['Host'] for j in jobs]
    return Counter(hosts)
