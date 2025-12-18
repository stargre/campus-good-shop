const fs = require('fs');
const path = require('path');
const { parse } = require('@vue/compiler-dom');

// 要检查的目录
const dirPath = path.resolve(__dirname, 'src');

// 递归遍历目录下的所有Vue文件
function traverseDir(dir, callback) {
  const files = fs.readdirSync(dir);
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stat = fs.statSync(filePath);
    if (stat.isDirectory()) {
      traverseDir(filePath, callback);
    } else if (file.endsWith('.vue')) {
      callback(filePath);
    }
  });
}

// 检查单个Vue文件
function checkVueFile(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    // 只检查template部分
    const templateMatch = content.match(/<template>([\s\S]*?)<\/template>/);
    if (templateMatch) {
      const templateContent = templateMatch[1];
      parse(templateContent);
      console.log(`✅ ${filePath}: No syntax errors`);
    }
  } catch (error) {
    console.error(`❌ ${filePath}: ${error.message}`);
  }
}

// 开始检查
console.log('Checking Vue files for syntax errors...');
traverseDir(dirPath, checkVueFile);
console.log('Check completed.');