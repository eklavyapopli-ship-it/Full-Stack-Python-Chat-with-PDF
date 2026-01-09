Sync - It waits until the process is complete
Async - Lets do this in background and let user do whatever he wants

QUEUES in System Design

Queue is a Data Structure based on FIFO(First in First out)
A consumer/ process will perform the work and give the user the results as soon as they are processed

For Queue system, we need Python RQ which uses Redis in the backend. 
Valkey is also an alternatibe to Redis
Running:
main.py
python -m rq.cli worker
To run worker in mac

export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES 
python3 -m rq.cli worker
