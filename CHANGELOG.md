# 1.1.0

 * [security] Rebuild image using latest upstream python:3.7-alpine tag to fix CVE-2019-5021 (#7)
 * [dependencies] Bump twisted from 18.9.0 to 19.2.1 (#6)

# 1.0.0

 * Expose four metrics from the filesystem:
   * `repository_tags_total`
   * `repository_revisions_total`
   * `repository_tag_layers_total`
   * `repository_tag_size_bytes`
