package pool

type Tasker interface {
    Execute()
}

type Task struct {
    id int
    data string
}

func NewTask(id int, data string) *Task {
    return &Task{
        id: id,
        data: data,
    }
}

func (t *Task) Execute() {
    //log.Printf("Task [%d] is executing: %s...", t.id, t.data)
}
