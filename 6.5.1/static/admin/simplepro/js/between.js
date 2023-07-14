Vue.component('between', {
    props: {
        value: {
            type: Array,
            default: function () {
                return [];
            }
        }
    },
    data() {
        return {
            field1: this.value[0],
            field2: this.value[1],
        }
    },
    watch: {
      value(newValue){
        this.field1 = newValue[0];
        this.field2 = newValue[1];
      }
    },
    methods: {
        change() {
            let value = [this.field1, this.field2];
            if (value[0] === "" && value[1] === "") {
                value = [];
            }
            this.$emit('input', value);
        }
    },
    template: `
    <div style="display: flex;justify-content: space-between;max-width: 200px;">
        <el-input v-model="field1" style="flex: 1" @change="change" clearable></el-input>
        <span style="margin: 0 5px;flex: 0 0 10px">-</span>
        <el-input v-model="field2" style="flex: 1" @change="change" clearable></el-input>
    </div>
    `
});