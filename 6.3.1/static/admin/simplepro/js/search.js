Vue.component('search', {
    props: ['data'],
    data() {
        let models = [];

        function deep(menus) {
            menus.forEach(item => {
                //这是首页，不显示
                if (item.eid === "1") {
                    return;
                }
                if (item.models) {
                    deep(item.models);
                } else {
                    models.push(item);
                }
            })

        }

        deep(this.data);

        return {
            show: false,
            input: '',
            models: models
        }
    },
    watch: {
        show: function () {
            this.input = '';
        }
    },
    methods: {
        querySearchAsync: function (queryString, cb) {

            var rs = this.models.filter(item => item.name.toLowerCase().indexOf(queryString.toLowerCase()) != -1);
            var values = [];
            rs.forEach(item => {
                values.push({
                    value: item.name,
                    item: item
                })
            });
            cb(values);
        },
        handleSelect: function (item) {
            app.openTab(item.item);
        },
        getClass() {
            return this.show ? 'header-search-in' : 'header-search-out';
        }
    },
    created() {
        document.addEventListener('click', __ => this.show = false)
    },
    template: '<span>' +
        '<el-button icon="el-icon-search" @click.stop="show=true" circle style="border:none"></el-button>' +
        '<el-autocomplete @select="handleSelect" :fetch-suggestions="querySearchAsync" :class="\'header-search \'+getClass()" @click.native.stop="show=true" size="small" placeholder="请输入内容" v-model="input" clearable> <template slot-scope="{ item }">\n' +
        '    <i :class="item.item.icon"></i>\n' +
        '    <span>{{ item.value }}</span>\n' +
        '  </template>' +
        '</el-autocomplete>' +
        '</span>'
});