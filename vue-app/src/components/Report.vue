<template>
    <div>

        <div>
            <form action="." method="post">
                <b-input id="dateInput" border-variant="outline-dark" class="mb-4 btn border border-secondary" type="date" v-model="theDate" value=""/> <br>
                <b-button variant="outline-primary" @click="submit">Get Report</b-button>
                <b-button variant="outline-primary" @click="clear">Report API</b-button>
            </form>
        </div>
        <div class="data">
            {{ api_data }}
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
                api_data: ''
            }
        },
        // template: '<div>{{ api_data }}</div>',

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