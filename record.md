### 关键库
langchain / 核心库

langchain-openai / 集成openai的langchain模型调用 

langchain-community / 和langchain适配的一些第三方库函数

### 遇到的问题
1. LLM对于行号不准确，有时会把代码加到错误的行，从而覆盖原有代码
   解决方案：
   1. prompt设计，行号的定义更清晰
   2. 能否探索不需要行号的？
   0617通过改prompt，暂没解决
   ~~2. LLM的输出怎么正确识别？~~(已解决)
   ~~1. 目前在用json，但是json要求都用双引号包裹，这就要求LLM的输出里，对于json的key必须用双引号包裹，而内容又必须用转义字符来把双引号转义。~~



### 解决方案

> **参考网址：**
>
> 【1】[LLM生成代码后，如何一键合并到源代码中（FastApply技术研究） - boydfd - 博客园](https://www.cnblogs.com/boydfd/p/18759542)
>
> 【2】[kortix-ai/fast-apply](https://github.com/kortix-ai/fast-apply)

1. ~~让LLM生成code diff，然后用第三方code diff 合并工具合并。~~

   结论：不可行，LLM对于数字不敏感，对于code diff的行号把握不准

   <img src="https://gitee.com/fancy_R/picgo-picture/raw/master/img/image-20250618161243950.png" alt="image-20250618161243950" style="zoom:50%;" />

2. 对于结构分明的代码块，利用 AST 进行section级别的替换

   结论：部分可行，取决于要修改的代码是否有分明的结构

<img src="https://gitee.com/fancy_R/picgo-picture/raw/master/img/image-20250618161303476.png" alt="image-20250618161303476" style="zoom:50%;" />

3. 全量代码替换

   LLM生成更新代码片段后，再和LLM原始代码一起，让LLM重新合并代码。

   结论：部分可行，速度慢。

4. 蒸馏小模型做合并

   LLM生成更新代码片段后，与原始代码一起，让一个蒸馏过的小模型来合并代码。

5. Speculative Decoding

   基于小模型合并的思路继续发展（貌似是不用蒸馏？），LLM生成更新代码片段后，与原始代码一起，让一个小模型来合并代码。

   小模型输出候选token序列后，LLM只做概率验证（基于条件概率并行验证），然后LLM选择接受还是拒绝小模型的token。理想情况下可以加速LLM推理过程。

6. Prompt Lookup Decoding

   **特殊应用条件：**输出和输入重叠很大，（例如这里的代码合并，输出的代码完全由原有代码+修改代码拼接而成）

   基于Speculative Decoding的思路，但是候选token不用小模型生成，而是直接从输入的prompt里按照一定规则找，这样连小模型的token生成时间都优化了。



---

**基于copilot的做法**

锚点+局部范围匹配

（被修改的代码的不变上下文作为锚点进行定位，在锚点往后搜索特定范围代码，如果匹配就进行替换；多个锚点+多个搜索，感觉不太可能发生；发生了就重新生成锚点，并且锚点范围增大）



**cursor的做法**

生成修改后代码的同时，附带对应的原代码，然后直接替换
