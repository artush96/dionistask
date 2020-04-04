<template>
    <div>

        <div>
            <form action="." method="post">
                <b-input id="dateInput" border-variant="outline-dark" class="mb-4 btn border border-secondary"
                         type="date" v-model="theDate" value=""/>
                <br>
                <b-button variant="outline-primary" @click="submit">Get Report</b-button>
                <b-button variant="outline-primary" @click="clear">Report API</b-button>
            </form>
        </div>
        <div class="data">
            <!--            {{ api_data }}-->
            <table class="table">
                <thead>
                <tr>
                    <th scope="col">#</th>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Surname</th>
                    <th scope="col">Middle Name</th>
                    <th scope="col">Payload</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="i in api_data">
                    <th scope="row">1</th>
                    <td>{{i.id}}</td>
                    <td>{{i.name}}</td>
                    <td>{{i.surname}}</td>
                    <td>{{i.middle_name}}</td>
                    <td>{{i.payload_by_date}}</td>
                </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    import Axios from 'axios'

    export default {
        name: "Report",
        data: () => ({
            theDate: '',
        }),
        data() {
            return {
                api_data: '',
            }
        },

        methods: {
            submit() {
                var url = 'http://127.0.0.1:8000/api';
                let headers = new Headers();
                // headers.append('Content-Type', 'application/json');
                // headers.append('Accept', 'application/json');

                headers.append('Access-Control-Allow-Origin', '*');
                headers.append('Access-Control-Allow-Methods', '*');
                headers.append('Access-Control-Allow-Headers', '*');

                Axios
                    .post(url, {theDate: this.theDate}, headers)
                    .then(response => (this.api_data = response.data))
            },
            clear() {

            }
        }
    }


</script>

<style scoped>
    #dateInput {
        width: auto;
    }

    .data {
        width: 40%;
        margin-top: 100px;

    }
</style>