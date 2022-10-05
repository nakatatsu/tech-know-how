---
Title: Terraformのディレクトリ設計方針
Category:
- Terraform
Date: 2022-10-05T15:06:27+09:00
URL: https://blog.tricrow.com/entry/terraform/terraform-code-structure-plan
EditURL: https://blog.hatena.ne.jp/good-one/good-one.hatenablog.com/atom/entry/4207112889924732234
---

Terraformのディレクトリ設計方針について記載する。

[:contents]

# 公式のベストプラクティス

Terraformのディレクトリ設計には、ベストプラクティスとして[公式が例を公開](https://www.terraform-best-practices.com/examples)してくれている。特に理由がなければそちらをベースにすれば良いだろう。


    https://github.com/antonbabenko/terraform-best-practices/tree/master/examples/medium-terraform
    │  README.md
    │
    ├─modules
    │  └─network
    │          main.tf
    │          outputs.tf
    │          variables.tf
    │
    ├─prod
    │      main.tf
    │      outputs.tf
    │      terraform.tfvars
    │      variables.tf
    │
    └─stage
            main.tf
            outputs.tf
            terraform.tfvars
            variables.tf


small/medium/largeの３種が公開されているが、たいていmediumを参考にすることになると思われる。smallは用途が限られるし、largeはまだ作りかけ（2022/10/05時点）のようだからだ。

多くの場合、リソース一式を環境の数だけ作る。つまり`環境 × リソース一式`のように作業することになる。そのため概念を"環境"と"リソース一式"で大きく分けられるように作ってあるのだろう。

# モジュールの粒度をどうするか？

ディレクトリの構成は環境とモジュールで大きく二つにわける――という方向性は、ほぼほぼ完成している。あるとしても、せいぜい環境をenvironments/ 以下に入れるかどうか、といったところだろう。

だがモジュールをどの粒度でまとめるのか、が大きな課題として浮かび上がる。それは結局、どの基準でまとめるか、ということでもある。
結論、基準にできるものとして次のようなものがある。

1. 更新頻度
2. 集約関係にあるか否か
3. サービス単位

## 更新頻度

いったん構築したらその後はほぼ触らないリソースと、その後も頻繁に更新するリソースがある。たとえばVPCやSESはいったん構築したらその後はほぼ触らない（環境ごとまるまる作り直す運用をしていなければ）。

一方でWAFやSecurityGroupsは、特定の固定IPに対する開放/閉鎖があったりするとかなり頻繁に更新をかけることになる。

これらはできれば別々にしたいところだ。

| 更新頻度 | リソース |
|---|---|
| 低 | VPCやSES、RDSなど |
| 高 | WAFやSecurityGroupsなど |

※ プロジェクトによって運用が違うため、頻度も変わりえる。あくまで一般的な例。


## 集約関係にあるか否か

UMLの集約にあたる関係にあるリソースが中には存在する。

例えばVPC。routing tableやsubnet, igw, Nat Gateway等のリソースも合わせてNetworkingとして作業することが多いだろう。

例えばSecurityGroups。グループとポリシーは別々に作成する。

こういったものは、別々に作成すると見通しが悪いだけでなく、思わぬバグの元となる。極力まとめて作成するほうがよい。

## サービス単位

マイクロサービスのように複数のサービスを管理している場合、素直に考えればサービスごとにまとめたいところだろう。

- service1
- service2


## ではどう整理するか

上記の基準は衝突する。

たとえば、マイクロサービスならservice1 - service2で互いに通信させることがあり得る。サービス単位で構築すると、SecurityGroupsはそれぞれのサービスごとにポリシー追加を行わねばならなくなる。だがこれは集約関係に反する。

したがって、優先順位をつけたり分類を細分化したりして、うまく整理してやらないといけないわけだが、結論、優先順位は次の順番になると考えている。

    集約関係にあるか否か > サービス単位 > 更新頻度

集約関係にあるリソースは最優先でまとめたい。バラバラになっていると問題を起こしやすいからだ。

おそらくVPCやSecurityGroupsあたりをサービス横断で先に作成することになるだろう。もしそれが問題になるようならさらにモジュールを細分化して対応してもいい。

次はサービス単位でまとめたい。やはり人間の認識として、サービス単位で概念を把握することが多いためだ。

最後が更新頻度で、これはまあよっぽど頻繁に更新するものだけ切りだせば十分かな、といったところ。他とまとめられていても――なぜか毎回更新されるような問題が起きでもしなければ――変更のないリソースは無視されるので大した問題ではない。


# モジュールのNestの是非

モジュールをネストさせるのはあまり好ましくない。依存関係が複雑になりやすいためだ。[公式のBestPractices](https://www.terraform-best-practices.com/code-structure)にも、

    Keep resource modules as plain as possible
    （意訳：　モジュールはなるべく平易にしよう）

とあるくらいである。

とはいえCodePipelineのように単体のリソースですら大変複雑なものも中には存在する。そういったものを都度書くのは嫌だ、と考えるのは至極当然である。

そのため、多用すべきではないが、どうしてもやらざるを得ないようなケースではNestさせる、という方向が落としどころではないか。


# 参考

- https://qiita.com/fukubaka0825/items/103c900a4072121bb4ae
