<template>
    <div>
        <div>
            <form action="." method="post">
                <b-input id="dateInput" border-variant="outline-dark" class="mb-4 btn border border-secondary"
                         type="date" v-model="theDate" value=""/>
                <br>
                <b-button variant="outline-primary" @click="submit">Get Report</b-button>
                            <a class="btn btn-primary ml-2" :href="api_data[0]" target="_blank">Download</a>
            </form>
        </div>
        <div class="chart">
            <canvas ref="canvas"></canvas>
        </div>
        <div class="data">
            <table class="table">
                <thead>
                <tr>
                    <th scope="col">ID</th>
                    <th scope="col">Name</th>
                    <th scope="col">Surname</th>
                    <th scope="col">Middle Name</th>
                    <th scope="col">Payload</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="i in api_data">
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
    import {Line} from 'vue-chartjs'

    export default {
        name: "Report",
        data: () => ({
            theDate: '',
        }),
        data() {
            return {
                api_data: '',
            };
        },
        extends: Line,

        methods: {
            submit() {
            var url = 'http://127.0.0.1:8000';
            let headers = new Headers();

            headers.append('Access-Control-Allow-Origin', '*');
            headers.append('Access-Control-Allow-Methods', '*');
            headers.append('Access-Control-Allow-Headers', '*');

            Axios
                .post(url, {theDate: this.theDate}, headers)
                .then(response => (this.api_data = response.data));
            },
        },
        updated() {
            this.renderChart({
                labels: this.api_data[2].label,
                datasets: [{
                    label: '# Worker Report',
                    data: this.api_data[1].dat,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.2)',
                        'rgba(54, 162, 235, 0.2)',
                        'rgba(255, 206, 86, 0.2)',
                        'rgba(75, 192, 192, 0.2)',
                        'rgba(153, 102, 255, 0.2)',
                        'rgba(255, 159, 64, 0.2)'
                    ],
                    borderColor: [
                        'rgba(255, 99, 132, 1)',
                        'rgba(54, 162, 235, 1)',
                        'rgba(255, 206, 86, 1)',
                        'rgba(75, 192, 192, 1)',
                        'rgba(153, 102, 255, 1)',
                        'rgba(255, 159, 64, 1)'
                    ],
                    borderWidth: 1
                }]
            })
        },
    }


</script>

<style scoped>
    #dateInput {
        width: auto;
    }

    .data {
        width: 90%;
        margin: 100px 5% 0 5%;

    }

    .chart {
        width: 90%;
        margin: 50px 5% 0 5%;
    }
</style>