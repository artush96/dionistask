<template>
    <div id="app">
        <h1>Worker Report</h1>
        <hr>
        <Report/>
    </div>
</template>

<script>
    import Report from "./components/Report";
    export default {
        name: 'App',
        components: {Report}
    }
</script>

<style>
    #app {
        font-family: Avenir, Helvetica, Arial, sans-serif;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
        text-align: center;
        color: #2c3e50;
        margin-top: 60px;
    }
</style>
