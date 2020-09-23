package pool

import (
	"sync"
)

var (
	defaultPoolCapacity = 128
)

type Dispatcher struct {
	size int
	queue chan Tasker
	queueWG sync.WaitGroup

	sync.Mutex
	killer chan struct{}
}

func NewDispatcher(size int) *Dispatcher {
	d := &Dispatcher{
		queue: make(chan Tasker, defaultPoolCapacity),
		killer: make(chan struct{}),
	}
	d.resize(size)
	return d
}

func (d *Dispatcher) resize(size int) {
	d.Lock()
	defer d.Unlock()

	for d.size < size {
		d.size++
		d.queueWG.Add(1)
		go d.worker()
	}
	for d.size > size {
		d.size--
		d.killer <- struct{}{}
	}
}

func (d *Dispatcher) worker() {
	defer d.queueWG.Done()
	for {
		select {
			case task, ok := <- d.queue:
				if !ok {
					return
				}
			task.Execute()
		case <- d.killer:
			return
		}
	}
}

func (d *Dispatcher) Put(t Tasker) {
	//log.Printf("Put new task in pool...")
	d.queue <- t
}

func (d *Dispatcher) Stop() {
	close(d.queue)
}

func (d *Dispatcher) Wait() {
	d.queueWG.Wait()
}
