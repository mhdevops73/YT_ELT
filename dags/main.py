from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import get_channel_playlist_id, get_video_ids, extract_video_data, save_to_json

local_tz = pendulum.timezone("Europe/Zurich")

default_args = {
    "owner": 'airflow',
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "email" : "mhenri73@gmail.com",
    "max_active_runs" : 1,
    "dagrun_timeout" : timedelta(hours=2),
    "start_date": datetime(2025, 8, 1, tzinfo=local_tz)
}

with DAG(
    dag_id='produce_json',
    default_args=default_args,
    description='DAG to produce JSON file',
    schedule='0 10 * * *',
    catchup=False
) as dag:

#Define tasks
    playlist_id = get_channel_playlist_id()
    video_ids = get_video_ids(playlist_id)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)

playlist_id >> video_ids >> video_data >> save_to_json

