<template>
    <div class="container">
        <div class="todo-list">
            <div class="todo header">
                <div>Task</div>
                <div>Priority</div>
                <div>Complete</div>
            </div>
            <div class="todo" v-for="todo in todos" :key="todo.created">
                <div>{{ todo.title }}</div>
                <div>{{ todo.priority }}</div>
                <div><button @click="completeTodo(todo.id)">Done</button></div>
            </div>
            <div class="todo new-todo-form">
                <div>
                    <input type="text" v-model="newTodoTitle" placeholder="Add todo...">
                </div>
                <div>
                    <select name="priority" v-model=newTodoPriority>
                        <option v-for="(value, key) in Priority" :key=value :value="value">
                            {{ value }}
                        </option>
                    </select>
                </div>
                <div>
                    <button @click="newTodo">Add</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import {DefaultApi, Priority} from '@/generated-api';
import {onMounted, ref} from "vue";

const todos = ref([])
const newTodoTitle = ref('')
const newTodoPriority = ref('')

const apiClient = new DefaultApi();

onMounted(() => {
    apiClient.listTodo().then((data) => {
        todos.value.push(...data)
    })
})

function newTodo() {
    const req = {
        createTodoRequest: {
            title: newTodoTitle.value,
            priority: newTodoPriority.value
        }
    }

    apiClient.createTodo(req)
        .then(res => {
            todos.value.push(res)
            newTodoTitle.value = ""
        })
        .catch(err => {
            console.error(err)
        })
}

function completeTodo(id) {
    const req = {
        todoId: id
    }
    apiClient.completeTodo(req)
        .then((resp) => {
            todos.value = todos.value.filter(todo => todo.id !== resp.id)
        })
        .catch(err => {
            console.error(err)
        })
}

</script>

<style scoped>
.container {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
}
.todo-list, .new-todo-form {
    display: grid;
    grid-template-columns: 1fr 1fr auto;
    gap: 10px;
}

.todo, .new-todo-form > div {
    display: contents;
}

.todo > div, .new-todo-form > div > * {
    padding: 5px;
}

.header {
    font-weight: bold;
}
</style>
