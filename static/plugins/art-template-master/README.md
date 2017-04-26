# art-template

[![NPM Version](https://img.shields.io/npm/v/art-template.svg)](https://npmjs.org/package/art-template)
[![Node.js Version](https://img.shields.io/node/v/art-template.svg)](http://nodejs.org/download/)
[![Travis-ci](https://travis-ci.org/aui/art-template.svg?branch=master)](https://travis-ci.org/aui/art-template)
[![Coverage Status](https://coveralls.io/repos/github/aui/art-template/badge.svg?branch=master)](https://coveralls.io/github/aui/art-template?branch=master)

art-template 是一个性能出众模板引擎，无论在 NodeJS 还是在浏览器中都可以运行。

![chart](https://cloud.githubusercontent.com/assets/1791748/24965783/aa044388-1fd7-11e7-9d45-43b0e7ff5d86.png)

[在线速度测试](http://aui.github.io/art-template/example/web-test-speed/)

## 特性

* 针对 V8 引擎优化，渲染速度出众
* 支持编译、运行时调试，可定位语法、渲染错误的模板语句
* 支持 NodeJS 与 浏览器。支持 Express、Koa、Webpack、RequireJS
* 支持模板包含与模板继承
* 兼容 [EJS](http://ejs.co)、[Underscore](http://underscorejs.org/#template)、[LoDash](https://lodash.com/docs/#template) 模板语法
* 支持 ES 严格模式环境运行
* 同时支持原生 JavaScript 语法、简约语法
* 支持定义模板的语法规则
* 浏览器版本仅 5KB 大小

## 安装

```shell
npm install art-template --save
```

## 快速入门

### 模板语法

```html
<% if (user) { %>
  <h2><%= user.name %></h2>
<% } %>

或：

{{if user}}
  <h2>{{user.name}}</h2>
{{/if}}
```

### NodeJS

```js
var template = require('art-template');
var html = template(__diranme + '/tpl-user.art', {
    user: {
        name: 'aui'
    }
});
```

框架支持：

* Express: [express-art-template](https://github.com/aui/express-art-template)
* Koa: [koa-art-template](https://github.com/aui/koa-art-template)

### Webpack

安装 [art-template-loader](https://github.com/aui/art-template-loader)

```js
var render = require('./tpl-user.art');
var html = render({
    user: {
        name: 'aui'
    }
});
```

### Web

使用浏览器版本：[lib/template-web.js](https://raw.githubusercontent.com/aui/art-template/master/lib/template-web.js)

```html
<script id="tpl-user" type="text/html">
<% if (user) { %>
  <h2><%= user.name %></h2>
<% } %>
</script>

<script src="art-template/lib/template-web.js"></script>
<script>
var html = template('tpl-user', {
    user: {
        name: 'aui'
    }
});
</script>
```

> [lib/template-web.js](https://raw.githubusercontent.com/aui/art-template/master/lib/template-web.js) 支持 [RequireJS](http://requirejs.org) 加载

### 核心方法

```js
// 基于模板名渲染模板
template(filename, data);

// 将模板源代码编译成函数
template.compile(source, options);

// 将模板源代码编译成函数并立刻执行
template.render(source, data, options);
```

## 语法

art-template 同时支持 `{{expression}}` 简约语法与任意 JavaScript 表达式 `<% expression %>`。

### 输出

**1\. 标准输出**

```html
{{value}}
{{a ? b : c}}
{{a || b}}
{{a + b}}

or

<%= value %>
<%= a ? b : c %>
<%= a || b %>
<%= a + b %>
```

特殊变量可以使用下标方式访问：

```
{{$data['user list']}}
```

**2\. 原始输出**

```html
{{@value}}

or

<%- value %>
```

原始输出语句不会对 `HTML` 内容进行转义

### 条件

```html
{{if value}} ... {{/if}}
{{if v1}} ... {{else if v2}} ... {{/if}}

or

<% if (value) { %> ... <% } %>
<% if (value) { %> ... <% } else { %> ... <% } %>
```

### 循环

```html
{{each target}}
    {{$index}} {{$value}}
{{/each}}

or

<% for(var i = 0; i < target.length; i++){ %>
    <%= i %> <%= target[i] %>
<% } %>
```

1. `target` 支持 `Array` 与 `Object` 的迭代，其默认值为 `$data`
2. `$value` 与 `$index` 可以自定义：`{{each target val key}}`

### 变量

```html
{{set temp = data.sub.content}}

or

<% var temp = data.sub.content; %> 
```

### 子模板

```html
{{include './header.art'}}
{{include './header.art' data}}

or

<% include('./header.art') %>
<% include('./header.art', data) %>
```

`include` 第二个参数默认值为 `$data`。

### 布局

```html
{{extend './layout.art'}}
{{block 'head'}} ... {{/block}}
```

模板继承允许你构建一个包含你站点共同元素的基本模板“骨架”。

#### 范例

layout.art:

```html
<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{block 'title'}}My Site{{/block}}</title>

    {{block 'head'}}
    <link rel="stylesheet" href="main.css">
    {{/block}}
</head>
<body>
    {{block 'content'}}{{/block}}
</body>
</html>
```

index.art:

```html
{{extend './layout.art'}}

{{block 'title'}}My Page{{/block}}

{{block 'head'}}
    {{@parent}}
    <link rel="stylesheet" href="custom.css">
{{/block}}

{{block 'content'}}
<p>This is just an awesome page.</p>
{{/block}}
```

渲染 index.art 后，将自动应用布局骨架。

### print

```html
<% print(val, val2, val3) %>
```

### 过滤器

```js
// 向模板中导入过滤器
template.defaults.imports.$dateFormat = function(date, format){/*[code..]*/};
template.defaults.imports.$timestamp = function(value){return value * 1000};
```

```html
{{date | $timestamp | $dateFormat 'yyyy-MM-dd hh:mm:ss'}}

or

<%= $dateFormat($timestamp(date), 'yyyy-MM-dd hh:mm:ss') %>
```

## 全局变量

### 内置变量

* `$data`     传入模板的数据 `{Object|array}`
* `$imports`  外部导入的所有变量，等同 `template.defaults.imports` `{Object}`
* `$options`  模板编译选项 `{Object}`
* `print`     字符串输出函数 `{function}`
* `include`   子模板载入函数 `{function}`
* `extend`    布局模板导入函数 `{function}`
* `block`     模板块声明函数 `{function}`

### 注入全局变量

```js
template.defaults.imports.$console = console;
```

```html
<% $console.log('hello world') %>
```

模板外部所有的变量都需要使用 `template.defaults.imports` 注入、并且要在模板编译之前进行声明才能使用。

## 缓存

缓存默认是开启的，开发环境中可以关闭它：

```js
template.defaults.cache = false;
```

## 定义语法规则

从一个简单的例子说起，让模板引擎支持 ES6 `${name}` 模板字符串的解析：

```js
template.defaults.rules.push({
    test: /\${([\w\W]*?)}/,
    use: function(match, code) {
        return {
            code: code,
            output: 'escape'
        }
    }
});
```

其中 `test` 是匹配字符串正则，`use` 是匹配后的调用函数。关于 `use` 函数：

* 参数：一个参数为匹配到的字符串，其余的参数依次接收 `test` 正则的分组匹配内容
* 返回值：必须返回一个对象，包含 `code` 与 `output` 两个字段：
    * `code` 转换后的 JavaScript 语句
    * `output` 描述 `code` 的类型，可选值：
        * `'escape'` 编码后进行输出
        * `'raw'` 输出原始内容
        * `false` 不输出任何内容

## 使用 `require(templatePath)`

加载 `.art` 模板：

```js
var template = require('art-template');
var view = require('./index.art');
var html = view(data); 
```

加载 `.ejs` 模板：

```js
var template = require('art-template');
require.extensions['.ejs'] = template.extension;

var view = require('./index.ejs');
var html = view(data); 
```

## API

###	template(filename, data)

根据模板名渲染模板。

```js
var html = template('/welcome.art', {
    value: 'aui'
});
```

> 在浏览器中，`filename` 请传入存放模板的元素 `id`

###	template(filename, source)

编译模板并缓存。

```js
// compile && cache
template('/welcome.art', 'hi, <%=value%>.');

// use
template('/welcome.art', {
    value: 'aui'
});
```

###	.compile(source, options)

编译模板并返回一个渲染函数。

```js
var render = template.compile('hi, <%=value%>.');
var html = render({value: 'aui'});
```

###	.render(source, data, options)

编译并返回渲染结果。

```js
var html = template.render('hi, <%=value%>.', {value: 'aui'});
```

###	.defaults

模板引擎默认配置。参考 [选项](#选项)。

## 选项

`template.defaults`

```js
{
    // 模板名字
    filename: null,

    // 模板语法规则列表
    rules: [nativeRule, artRule],

    // 是否支持对模板输出语句进行编码。为 false 则关闭编码输出功能
    escape: true,

    // 是否开启调试模式。如果为 true: {bail:false, cache:false, compileDebug:true}
    debug: false,

    // 是否开启缓存
    cache: true,

    // 是否编译调试版。编译为调试版本可以在运行时进行 DEBUG
    compileDebug: false,

    // 是否容错。如果为 true，编译错误与运行时错误都会抛出异常
    bail: false,

    // 模板路径转换器
    resolveFilename: resolveFilename,

    // HTML 压缩器
    compressor: null,

    // 错误调试器
    debuger: debuger,

    // 模板文件加载器
    loader: loader,

    // 缓存中心适配器（依赖 filename 字段）
    caches: caches,

    // 模板根目录。如果 filename 为全局路径，则会基于此查找模板
    root: '/',

    // 默认后缀名。如果没有后缀名，则会自动基于此补全
    extname: '.art',

    // 导入的模板变量
    imports: {
        $each: each,
        $escape: escape,
        $include: include
    }
};
```

## 兼容性

1. NodeJS v1.0+
2. IE9+（小于 IE9 需要 [es5-shim](https://github.com/es-shims/es5-shim) 和 [JSON](https://github.com/douglascrockford/JSON-js) 支持）

## 授权协议

[MIT](./LICENSE)