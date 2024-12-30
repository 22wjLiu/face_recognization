// 模拟 API 请求（可以根据实际需要与后端 API 对接）

// 获取班级列表
export const getClassList = () => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: [
            { id: '1', name: '班级A' },
            { id: '2', name: '班级B' },
            { id: '3', name: '班级C' },
          ],
          message: '成功获取班级列表',
          success: true,
        });
      }, 1000);
    });
  };
  
  // 创建班级
  export const createClass = (classData) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: { ...classData, id: String(Math.random()) }, // 假设返回新增的班级信息，生成一个随机的 id
          message: '班级创建成功',
          success: true,
        });
      }, 1000);
    });
  };
  
  // 更新班级
  export const updateClass = (classData) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: classData,
          message: '班级更新成功',
          success: true,
        });
      }, 1000);
    });
  };
  
  // 删除班级
  export const deleteClass = (classId) => {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          data: { id: classId },
          message: '班级删除成功',
          success: true,
        });
      }, 1000);
    });
  };
  