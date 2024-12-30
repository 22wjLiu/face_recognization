<template>
  <div class="app-container">
    <div class="content">
      <!-- 左侧班级管理 -->
      <div class="left-sidebar">
        <el-button
          class="filter-item"
          style="margin-left: 10px; margin-bottom: 20px;"
          type="primary"
          icon="el-icon-edit"
          @click="handleClassCreate"
        >
          qusi
        </el-button>

        <el-table
          :data="classList"
          border
          fit
          highlight-current-row
          style="width: 100%;"
          @row-click="handleClassClick"
        >
          <el-table-column label="班级名称" prop="name" align="center" width="170">
            <template slot-scope="{ row }">
              <span>{{ row.name }}</span>
            </template>
          </el-table-column>

          <el-table-column label="操作" align="center" width="170">
            <template slot-scope="{ row }">
              <el-button
                size="mini"
                type="danger"
                @click="handleClassDelete(row)"
              >
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>

      <!-- 右侧学生信息 -->
      <div class="right-content">
        <el-button
          class="filter-item"
          style="margin-left: 10px; margin-bottom: 20px;"
          type="primary"
          icon="el-icon-edit"
          @click="handleCreate"
        >
          添加学生
        </el-button>

        <el-table
          :key="tableKey"
          v-loading="listLoading"
          :data="list"
          border
          fit
          highlight-current-row
          style="width: 89%;"
          @sort-change="sortChange"
        >
          <el-table-column label="学号" prop="id" sortable="custom" align="center" width="240">
            <template slot-scope="{ row }">
              <span>{{ row.id }}</span>
            </template>
          </el-table-column>
          <el-table-column label="学生姓名" width="300px" align="center">
            <template slot-scope="{ row }">
              <span>{{ row.author }}</span>
            </template>
          </el-table-column>
          <el-table-column label="操作" align="center" width="250" class-name="small-padding fixed-width">
            <template slot-scope="{ row, $index }">
              <el-button type="primary" size="mini" @click="handleUpdate(row)">
                修改
              </el-button>
              <el-button size="mini" type="danger" @click="handleDelete(row, $index)">
                删除
              </el-button>
            </template>
          </el-table-column>
        </el-table>

        <!-- 添加/更新学生信息对话框 -->
        <el-dialog :title="dialogTitle" :visible.sync="dialogFormVisible">
          <el-form ref="dataForm" :rules="rules" :model="temp" label-position="left" label-width="70px" style="width: 450px; margin-left: 50px;">
            <el-form-item label="学号" prop="id">
              <el-input v-model="temp.id" placeholder="请输入学号" />
            </el-form-item>
            <el-form-item label="姓名" prop="author">
              <el-input v-model="temp.author" placeholder="请输入姓名" />
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogFormVisible = false">
              取消
            </el-button>
            <el-button type="primary" @click="dialogStatus === 'create' ? createData() : updateData()">
              确定
            </el-button>
          </div>
        </el-dialog>

        <!-- 编辑班级对话框 -->
        <el-dialog :title="dialogClassTitle" :visible.sync="dialogClassFormVisible">
          <el-form ref="classForm" :rules="classRules" :model="classTemp" label-position="left" label-width="70px" style="width: 400px; margin-left: 50px;">
            <el-form-item label="班级名称" prop="name">
              <el-input v-model="classTemp.name" placeholder="请输入班级名称" />
            </el-form-item>
          </el-form>
          <div slot="footer" class="dialog-footer">
            <el-button @click="dialogClassFormVisible = false">
              取消
            </el-button>
            <el-button type="primary" @click="dialogClassStatus === 'create' ? createClass() : updateClass()">
              确定
            </el-button>
          </div>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import { getClassList, createClass, updateClass, deleteClass } from '@/api/class'
import Pagination from '@/components/Pagination'

export default {
  name: 'ClassStudentManagement',
  components: { Pagination },
  data() {
    return {
      tableKey: 0,
      list: [],
      total: 0,
      classList: [],
      listLoading: true,
      listQuery: {
        page: 1,
        limit: 20
      },
      dialogFormVisible: false,
      dialogStatus: '',
      temp: {
        id: undefined,
        author: '',
        classId: undefined
      },
      dialogClassFormVisible: false,
      dialogClassStatus: '',
      classTemp: {
        name: ''
      },
      rules: {
        id: [{ required: true, message: '学号不能为空', trigger: 'blur' }],
        author: [{ required: true, message: '姓名不能为空', trigger: 'blur' }]
      },
      classRules: {
        name: [{ required: true, message: '班级名称不能为空', trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getClassList()
  },
  methods: {
    // 获取班级列表
    getClassList() {
      this.listLoading = true
      getClassList().then((response) => {
        if (response.success) {
          this.classList = response.data
          this.listLoading = false
        }
      })
    },

    // 获取学生列表
    getList() {
      this.listLoading = true
      setTimeout(() => {
        this.list = [
          { id: '1001', author: '学生A', classId: this.temp.classId },
          { id: '1002', author: '学生B', classId: this.temp.classId }
        ]
        this.total = this.list.length
        this.listLoading = false
      }, 1000)
    },

    // 选择班级后更新学生列表
    handleClassClick(row) {
      this.temp.classId = row.id
      this.getList()
    },

    // 打开编辑班级对话框
    handleClassCreate() {
      this.classTemp = { name: '' }
      this.dialogClassStatus = 'create'
      this.dialogClassFormVisible = true
    },

    // 创建班级
    createClass() {
      if (this.classTemp.name) {
        createClass(this.classTemp).then((response) => {
          if (response.success) {
            this.classList.push(response.data) // 更新班级列表
            this.dialogClassFormVisible = false
            this.$message.success('班级创建成功')
          }
        })
      }
    },

    // 删除班级
    handleClassDelete(row) {
      this.$confirm(`确定要删除班级: ${row.name} 吗?`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        deleteClass(row.id).then((response) => {
          if (response.success) {
            this.classList = this.classList.filter(item => item.id !== row.id)
            this.$message.success('班级删除成功')
          }
        })
      })
    },

    // 打开添加学生对话框
    handleCreate() {
      this.temp = {
        id: undefined,
        author: '',
        classId: this.temp.classId
      }
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
    },

    // 创建学生
    createData() {
      console.log(this.temp)
      this.dialogFormVisible = false
    },

    // 更新学生
    updateData() {
      console.log(this.temp)
      this.dialogFormVisible = false
    },

    // 删除学生
    handleDelete(row, index) {
      this.list.splice(index, 1)
      this.$message.success('删除成功')
    },

    // 更新学生信息
    handleUpdate(row) {
      this.temp = { ...row }
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
    }
  }
}
</script>

<style scoped>
.app-container {
  display: flex;
  justify-content: space-between;
  padding: 20px;
}

.content {
  display: flex;
  width: 100%;
}

.left-sidebar {
  width: 361px;

  padding-right: 20px;
}

.right-content {
  flex-grow: 1;
  padding-left: 20px;
}

.dialog-footer {
  text-align: center;
  margin-top: 20px;
}
</style>
