#!/usr/bin/env python3
"""
adapt_susfs_patch.py
Dynamically adapts 50_add_susfs_in_gki-${version}.patch to match the target kernel source tree.

Handles kernel sublevel discrepancies across Linux 6.12 versions:
1. fs/exec.c: Checks for presence of <linux/dma-buf.h> and aligns patch context lines.
2. fs/proc/task_mmu.c: Checks for vma_pages(vma) vs vma_data_pages(vma) in show_smap.
3. fs/proc/task_mmu.c: Detects legacy show_smaps_rollup loop (sublevel < 69/92) vs
   modern show_smaps_rollup loop (sublevel 92+) and substitutes matching SUSFS hunks.
"""

import argparse
import os
import sys

# Legacy show_smaps_rollup hunk for kernel 6.12.30 (sublevel < 69/92)
OLD_ROLLUP_HUNK = """@@ -1388,7 +1437,14 @@ static int show_smaps_rollup(struct seq_file *m, void *v)
 
 	vma_start = vma->vm_start;
 	do {
+#ifdef CONFIG_KSU_SUSFS_SUS_MAP
+		if (vma->vm_file && SUSFS_IS_INODE_SUS_MAP(file_inode(vma->vm_file)))
+			goto bypass_orig_flow;
+#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MAP
 		smap_gather_stats(vma, &mss, 0);
+#ifdef CONFIG_KSU_SUSFS_SUS_MAP
+bypass_orig_flow:
+#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MAP
 		last_vma_end = vma->vm_end;
 
 		/*
@@ -1454,8 +1510,15 @@ static int show_smaps_rollup(struct seq_file *m, void *v)
 
 			/* Case 4 above */
 			if (vma->vm_end > last_vma_end) {
+#ifdef CONFIG_KSU_SUSFS_SUS_MAP
+				if (!vma->vm_file || !(SUSFS_IS_INODE_SUS_MAP(file_inode(vma->vm_file)))) {
+					smap_gather_stats(vma, &mss, last_vma_end);
+					last_vma_end = vma->vm_end;
+				}
+#else
 				smap_gather_stats(vma, &mss, last_vma_end);
 				last_vma_end = vma->vm_end;
+#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MAP
 			}
 		}
 	} for_each_vma(vmi, vma);
"""

# Modern show_smaps_rollup hunk for kernel 6.12.92+
NEW_ROLLUP_HUNK = """@@ -1618,6 +1667,11 @@ static int show_smaps_rollup(struct seq_file *m, void *v)
 			goto out_unlock;
 		}
 
+#ifdef CONFIG_KSU_SUSFS_SUS_MAP
+		if (vma->vm_file && SUSFS_IS_INODE_SUS_MAP(file_inode(vma->vm_file)))
+			goto bypass_orig_flow;
+#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MAP
+
 		if (vma->vm_start < last_vma_end) {
 			/*
 			 * After retaking the lock, already reported VMA grew
@@ -1630,6 +1684,9 @@ static int show_smaps_rollup(struct seq_file *m, void *v)
 			/* Found next unreported VMA, start from its beginning */
 			smap_gather_stats(priv, vma, &mss);
 		}
+#ifdef CONFIG_KSU_SUSFS_SUS_MAP
+bypass_orig_flow:
+#endif // #ifdef CONFIG_KSU_SUSFS_SUS_MAP
 		last_vma_end = vma->vm_end;
 
 		/*
"""


def adapt_patch(patch_path: str, kernel_dir: str) -> None:
    if not os.path.isfile(patch_path):
        print(f"[ERROR] Patch file not found: {patch_path}", file=sys.stderr)
        sys.exit(1)

    with open(patch_path, "r", encoding="utf-8", errors="replace") as f:
        patch_text = f.read()

    modified = False

    # 1. fs/exec.c: dma-buf.h context line alignment
    exec_path = os.path.join(kernel_dir, "fs", "exec.c")
    if os.path.isfile(exec_path):
        with open(exec_path, "r", encoding="utf-8", errors="replace") as f:
            exec_c = f.read()

        exec_has_dmabuf = "<linux/dma-buf.h>" in exec_c
        patch_has_dmabuf = " #include <linux/dma-buf.h>\n+#ifdef CONFIG_KSU_SUSFS" in patch_text

        if not exec_has_dmabuf and patch_has_dmabuf:
            print("[INFO] Kernel fs/exec.c lacks dma-buf.h; removing context line from patch...")
            patch_text = patch_text.replace(
                "@@ -70,6 +70,9 @@",
                "@@ -70,5 +70,8 @@",
            )
            patch_text = patch_text.replace(
                " #include <linux/dma-buf.h>\n+#ifdef CONFIG_KSU_SUSFS",
                "+#ifdef CONFIG_KSU_SUSFS",
            )
            modified = True
        elif exec_has_dmabuf and not patch_has_dmabuf and " #include <linux/ksm.h>\n+#ifdef CONFIG_KSU_SUSFS" in patch_text:
            print("[INFO] Kernel fs/exec.c has dma-buf.h; adding context line to patch...")
            patch_text = patch_text.replace(
                "@@ -70,5 +70,8 @@",
                "@@ -70,6 +70,9 @@",
            )
            patch_text = patch_text.replace(
                " #include <linux/ksm.h>\n+#ifdef CONFIG_KSU_SUSFS",
                " #include <linux/ksm.h>\n #include <linux/dma-buf.h>\n+#ifdef CONFIG_KSU_SUSFS",
            )
            modified = True

    # 2. fs/proc/task_mmu.c: vma_data_pages vs vma_pages in show_smap
    task_mmu_path = os.path.join(kernel_dir, "fs", "proc", "task_mmu.c")
    if os.path.isfile(task_mmu_path):
        with open(task_mmu_path, "r", encoding="utf-8", errors="replace") as f:
            task_mmu_c = f.read()

        task_mmu_has_vma_data_pages = "vma_data_pages(vma)" in task_mmu_c
        patch_has_vma_data_pages = " \tif (!vma_data_pages(vma))" in patch_text
        patch_has_vma_pages = " \tif (!vma_pages(vma))" in patch_text

        if not task_mmu_has_vma_data_pages and patch_has_vma_data_pages:
            print("[INFO] Kernel task_mmu.c uses vma_pages; adapting patch show_smap context...")
            patch_text = patch_text.replace(
                " \tif (!vma_data_pages(vma))",
                " \tif (!vma_pages(vma))",
            )
            modified = True
        elif task_mmu_has_vma_data_pages and patch_has_vma_pages:
            print("[INFO] Kernel task_mmu.c uses vma_data_pages; adapting patch show_smap context...")
            patch_text = patch_text.replace(
                " \tif (!vma_pages(vma))",
                " \tif (!vma_data_pages(vma))",
            )
            modified = True

        # 3. fs/proc/task_mmu.c: show_smaps_rollup hunk alignment
        kernel_has_old_rollup = "smap_gather_stats(vma, &mss, 0);" in task_mmu_c
        patch_has_new_rollup = "smap_gather_stats(priv, vma, &mss);" in patch_text
        patch_has_old_rollup = "smap_gather_stats(vma, &mss, 0);" in patch_text

        if kernel_has_old_rollup and patch_has_new_rollup:
            if NEW_ROLLUP_HUNK in patch_text:
                print("[INFO] Kernel has legacy smaps_rollup loop; substituting legacy SUSFS rollup hunks...")
                patch_text = patch_text.replace(NEW_ROLLUP_HUNK, OLD_ROLLUP_HUNK)
                modified = True
            else:
                print("[WARN] NEW_ROLLUP_HUNK not found as exact block; searching hunk markers...")
                # Fallback: replace the body between the markers
                start_marker = "@@ -1618,6 +1667,11 @@ static int show_smaps_rollup"
                end_marker = "@@ -2449,6 +2506,9 @@ static ssize_t pagemap_read"
                s_idx = patch_text.find(start_marker)
                e_idx = patch_text.find(end_marker)
                if s_idx != -1 and e_idx != -1 and s_idx < e_idx:
                    patch_text = patch_text[:s_idx] + OLD_ROLLUP_HUNK + patch_text[e_idx:]
                    modified = True
                    print("[INFO] Successfully substituted legacy SUSFS rollup hunks via markers.")
        elif not kernel_has_old_rollup and patch_has_old_rollup:
            if OLD_ROLLUP_HUNK in patch_text:
                print("[INFO] Kernel has modern smaps_rollup loop; substituting modern SUSFS rollup hunks...")
                patch_text = patch_text.replace(OLD_ROLLUP_HUNK, NEW_ROLLUP_HUNK)
                modified = True

    if modified:
        with open(patch_path, "w", encoding="utf-8") as f:
            f.write(patch_text)
        print(f"[SUCCESS] Successfully adapted SUSFS patch: {patch_path}")
    else:
        print("[INFO] SUSFS patch already matches kernel source tree; no adaptation needed.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Adapt SUSFS patch to target kernel sublevel.")
    parser.add_argument("--patch", required=True, help="Path to 50_add_susfs_in_gki-*.patch")
    parser.add_argument("--kernel-dir", default=".", help="Path to kernel source root (e.g. kernel/common)")
    args = parser.parse_args()

    adapt_patch(args.patch, args.kernel_dir)


if __name__ == "__main__":
    main()
