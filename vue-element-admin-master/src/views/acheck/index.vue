<template>
  <div class="app-container">
    <div class="filter-container">
      <el-input v-model="listQuery.name" placeholder="考勤名称" style="width: 200px;" class="filter-item" @keyup.enter.native="handleFilter" />
      <el-button v-waves class="filter-item" type="primary" icon="el-icon-search" @click="handleFilter">
        查询
      </el-button>
      <el-button class="filter-item" style="margin-left: 10px;" type="primary" icon="el-icon-edit" @click="handleCreate">
        发起考勤
      </el-button>
    </div>

    <!-- 表格 -->
    <el-table
      :key="tableKey"
      v-loading="listLoading"
      :data="list"
      border
      fit
      highlight-current-row
      style="width: 100%;">
      <el-table-column label="ID" prop="id"  align="center" width="100" :class-name="getSortClass('id')">
        <template slot-scope="{row}">
          <span>{{ row.id }}</span>
        </template>
      </el-table-column>

      <el-table-column label="截止时间" width="200px" align="center">
        <template slot-scope="{row}">
          <span>{{ row.timestamp | parseTime('{y}-{m}-{d} {h}:{i}') }}</span>
        </template>
      </el-table-column>

      <el-table-column label="考勤名称" width="600px" align="center">
        <template slot-scope="{row}">
          <span class="link-type" @click="handleUpdate(row)">{{ row.title }}</span>
          <el-tag>{{ row.type | typeFilter }}</el-tag>
        </template>
      </el-table-column>

      <el-table-column label="操作" align="center" width="350px" class-name="small-padding fixed-width">
        <template slot-scope="{row,$index}">
          <el-button type="primary" size="mini" @click="handleImgViews()">
            上传考勤照片
          </el-button>
          <el-button type="primary" size="mini" @click="detailViews()" style="margin-left:20px ;">
            结果详情
          </el-button>
          <el-button v-if="row.status!='deleted'" size="mini" type="danger" style="margin-left:20px ;" @click="handleDelete(row,$index)">
            删除考勤
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total>0" :total="total" :page.sync="listQuery.page" :limit.sync="listQuery.limit" @pagination="getList" />

    <!-- 上传考勤图片弹窗 -->
    <el-dialog :title="dialogUploadimg" :visible.sync="ImgFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temper" label-position="left" label-width="100px">
      
        <el-upload
        action="getRequestHeader() + '/upload?s_id=' + temper.id"
        list-type="picture-card"
        :auto-upload="false"
        :on-success="handleAvatarSuccess"
        :before-upload="beforeAvatarUpload">
          <i slot="default" class="el-icon-plus"></i>
            <div slot="file" slot-scope="{file}">
              <img
                class="el-upload-list__item-thumbnail"
                :src="file.url" alt=""
              >
            </div>
        </el-upload>
        <el-dialog :visible.sync="dialogVisible">
          <img width="100%" :src="dialogImageUrl" alt="">
        </el-dialog>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="ImgFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createImgData():updateImgData()">
          确定
        </el-button>
      </div>
    </el-dialog>

      <!-- 考勤发起弹窗 -->
      <el-dialog :title="textMap[dialogStatus]" :visible.sync="dialogFormVisible">
      <el-form ref="dataForm" :rules="rules" :model="temper" label-position="left" label-width="125px">

        <el-form-item label="考勤结束时间" prop="timestamp">
          <el-date-picker v-model="temper.timestamp" type="datetime" placeholder="Please pick a date" />
        </el-form-item>

        <el-form-item label=" 考勤的名称" prop="title">
          <el-input v-model="temper.title" />
        </el-form-item>

        <el-form-item label="选择考勤班级" prop="type">
          <el-select v-model="temper.type" class="filter-item" placeholder="Please select">
            <el-option v-for="item in calendarTypeOptions" :key="item.key" :label="item.display_name" :value="item.key" />
          </el-select>
        </el-form-item>

      </el-form>

      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">
          取消
        </el-button>
        <el-button type="primary" @click="dialogStatus==='create'?createData():updateData()">
          确定
        </el-button>
      </div>
    </el-dialog>

    <!-- 考勤详情弹窗 -->
    <el-dialog :title="dialogTitle" :visible.sync="detailFormVisible" > 
         
           <el-table
          :key="tableKey"
          v-loading="listLoading"
          :data="list"
          border
          fit
          highlight-current-row
          height="500px"
          style="width: 100%;"
          :row-class-name="tableRowClassName"><!--排序监听-->

          <el-table-column
            label="学号"
            prop="id"
            align="center"
            width="200"
            :class-name="getSortClass('id')"
          >
            <template slot-scope="{row}">
              <span>{{ row.id }}</span>
            </template>
          </el-table-column>

        <el-table-column
          label="学生姓名"
          prop="author"
          align="center"
          width="250"
          :class-name="getSortClass('id')"
        >
          <template slot-scope="{row}">
            <span>{{ row.author }}</span>
          </template>
        </el-table-column>

        <el-table-column
          label="考勤状态"
          prop="author"
          align="center"
          width="250"
          :class-name="getSortClass('id')"
        >
          <template slot-scope="{row}">
            <span>{{ row.status }}</span>
          </template>
        </el-table-column>

      </el-table>
    </el-dialog>

  </div>
</template>

<script>
import { fetchList, createArticle, updateArticle } from '@/api/article'
import waves from '@/directive/waves' // waves directive
import { parseTime } from '@/utils'
import Pagination from '@/components/Pagination' // secondary package based on el-pagination

const calendarTypeOptions = [
  { key: 'CN', display_name: '一班' },
  { key: 'US', display_name: '二班' },
  { key: 'JP', display_name: '三班' },
  { key: 'EU', display_name: '四班' }
]

// arr to obj, such as { CN : "China", US : "USA" }
const calendarTypeKeyValue = calendarTypeOptions.reduce((acc, cur) => {
  acc[cur.key] = cur.display_name
  return acc
}, {})

export default {
  name: 'ComplexTable',
  components: { Pagination },
  directives: { waves },
  filters: {
    statusFilter(status) {
      const statusMap = {
        published: 'success',
        draft: 'info',
        deleted: 'danger'
      }
      return statusMap[status]
    },
    typeFilter(type) {
      return calendarTypeKeyValue[type]
    }
  },
  data() {
    return {
      dialogImageUrl: '',
      dialogVisible: false,
      disabled: false,/**图片上传 */
      tableKey: 0,
      list: null,
      total: 0,
      listLoading: true,
      listQuery: {
        author: undefined, /** 学生姓名 */
        page: 1,
        limit: 20,
        importance: undefined,
        title: undefined,
        type: undefined,
        sort: '+id'
      },
      importanceOptions: [1, 2, 3],
      calendarTypeOptions,
      sortOptions: [{ label: 'ID Ascending', key: '+id' }, { label: 'ID Descending', key: '-id' }],
      statusOptions: ['punished', 'draft', 'deleted'],
      showReviewer: false,
      temper: {
        id: undefined,
        author: '', /* 学生姓名 */
        importance: 1,
        remark: '',
        timestamp: new Date(),
        title: '',
        type: '',
        status: '1'
      },
      dialogFormVisible: false,
      detailFormVisible: false,
      ImgFormVisible:false,
      dialogStatus: '',
      dialogTitle: '详细信息',
      dialogUploadimg:'上传考勤图片',
      textMap: {
        update: '编辑',
        create: '创建'
      },
      pvData: [],
      rules: {
        type: [{ required: true, message: 'type is required', trigger: 'change' }],
        timestamp: [{ type: 'date', required: true, message: 'timestamp is required', trigger: 'change' }],
        title: [{ required: true, message: 'title is required', trigger: 'blur' }]
      },
      downloadLoading: false
    }
  },
  created() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      fetchList(this.listQuery).then(response => {
        console.log('Fetched data:', response.data.items) // 打印数据
        this.list = response.data.items
        this.total = response.data.total
        this.listLoading = false // 确保加载状态关闭

        // Just to simulate the time of the request
        setTimeout(() => {
          this.listLoading = false
        }, 1.5 * 1000)
      })
    },
    handleFilter() {
      this.listQuery.page = 1
      this.getList()
    },
    resetTemp() {
      this.temper = {
        id: undefined,
        timestamp: new Date(),
        title: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          this.temper.id = parseInt(Math.random() * 100) + 1024 // mock a id
          this.temper.author = '李心情' /* 自拟一个？？？ */
          createArticle(this.temper).then(() => {
            this.list.unshift(this.temper)
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '发布考勤成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    createImgData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          request.post('student/addStudent', this.temp).then(() => {
            this.ImgFormVisible = false
            this.getList()
            this.$notify({
              title: '成功',
              message: '图片上传成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleUpdate(row) {
      this.temper = Object.assign({}, row) // copy obj
      this.temper.timestamp = new Date(this.temper.timestamp)
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.temper)
          tempData.timestamp = +new Date(tempData.timestamp) // change Thu Nov 30 2017 16:41:05 GMT+0800 (CST) to 1512031311464
          updateArticle(tempData).then(() => {
            const index = this.list.findIndex(v => v.id === this.temper.id)
            this.list.splice(index, 1, this.temper)
            this.dialogFormVisible = false
            this.$notify({
              title: '成功',
              message: '编辑考勤成功',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    updateImgData() {
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          request.post('student/updateStudent', this.temp).then(() => {
            this.dialogFormVisible = false
            this.getList()
            this.$notify({
              title: '成功',
              message: '考勤图片上传成功！',
              type: 'success',
              duration: 2000
            })
          })
        }
      })
    },
    handleDelete(row, index) {
      this.$notify({
        title: '成功',
        message: '提交删除请求成功，请等待服务器响应',
        type: 'success',
        duration: 2000
      })
      // this.list.splice(index, 1)
      request.delete('feature/deleteById', {
        params: {
          id: row.id
        }
      }).then(() => {
        this.getFeatureList(this.temper.id)
        this.$notify({
          title: '成功',
          message: '删除成功！',
          type: 'success',
          duration: 2000
        })
      })
    },
    getSortClass: function(key) {
      const sort = this.listQuery.sort
      return sort === `+${key}` ? 'ascending' : 'descending'
    },
    detailViews() { // 考勤详细信息
      this.resetTemp()
      this.dialogTitle = '考勤详细信息'
      this.detailFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    handleImgViews(){
      this.resetTemp()
      this.dialogTitle = '上传考勤图片'
      this.ImgFormVisible = true /**关闭弹窗 */
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    // 考勤颜色区分
    tableRowClassName(row) {
        if ( row.row.status === '0') {
          console.log(row.row.status)
          return 'warning-row';
        }
        return '';
      },
    handleAvatarSuccess(res) {/*考勤图片上传 */
      this.imageUrl = res.data
      this.$notify({
        title: '成功',
        message: '上传考勤照片成功！',
        type: 'success',
        duration: 2000
      })
      this.getFeatureList(this.temp.id)
    },
    beforeAvatarUpload(file) {
      const isJPG = file.type === 'image/jpeg' || 'image/png'
      const isLt2M = file.size / 1024 / 1024 < 2


      if (!isJPG) {
        this.$message.error('上传头像图片只能是 JPG 格式!')
      }
      if (!isLt2M) {
        this.$message.error('上传头像图片大小不能超过 2MB!')
      }
      this.$notify({
        title: '成功',
        message: '提交上传请求成功，请等待服务器响应！',
        type: 'success',
        duration: 2000
      })
      return isJPG && isLt2M
    }
  }
}
</script>

<style scoped>
::v-deep  .el-table .warning-row {
    background:oldlace !important;
  }
</style>

