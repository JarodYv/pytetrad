# PAG简介

FCI算法输出的是一个偏祖系图（partial ancestral graph），简称PAG。
PAG是一个图对象用于表示一组无法被算法区分的因果贝叶斯网络（CBN）。
假设我们有一组从某个因果贝叶斯网络随机采样生成的案例，在FCI算法的假设下，FCI返回的PAG保证包含生成这些数据的CBN。

图2是PAG的一个具体例子。

PAG中存在4种类型的边：$A \rarr B, A \circ \rarr B, A \circ-\circ B, A \leftrightarrow B$