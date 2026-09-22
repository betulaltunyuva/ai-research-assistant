from threading import Lock


_status_lock = Lock()

_job_statuses = {}


AGENTS = [
    "researcher",
    "analyst",
    "writer",
    "verifier"
]


def create_job_status(job_id: str):
    with _status_lock:
        _job_statuses[job_id] = {
            "status": "waiting",
            "agents": {
                agent: "waiting"
                for agent in AGENTS
            },
            "result": None,
            "error": None
        }


def update_job_status(
    job_id: str,
    status: str
):
    if not job_id:
        return

    with _status_lock:
        if job_id not in _job_statuses:
            return

        _job_statuses[job_id]["status"] = status


def update_agent_status(
    job_id: str,
    agent_name: str,
    status: str
):
    if not job_id:
        return

    with _status_lock:
        if job_id not in _job_statuses:
            return

        if agent_name not in AGENTS:
            return

        _job_statuses[job_id]["agents"][
            agent_name
        ] = status


def save_job_result(
    job_id: str,
    result: dict
):
    with _status_lock:
        if job_id not in _job_statuses:
            return

        _job_statuses[job_id]["result"] = result
        _job_statuses[job_id]["status"] = "completed"


def save_job_error(
    job_id: str,
    error: str
):
    with _status_lock:
        if job_id not in _job_statuses:
            return

        _job_statuses[job_id]["error"] = error
        _job_statuses[job_id]["status"] = "failed"


def get_job_status(
    job_id: str
):
    with _status_lock:
        status = _job_statuses.get(
            job_id
        )

        if status is None:
            return None

        return {
            "status": status["status"],
            "agents": dict(
                status["agents"]
            ),
            "result": status["result"],
            "error": status["error"]
        }