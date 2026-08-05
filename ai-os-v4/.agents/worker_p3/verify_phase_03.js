const fs = require('fs');
const path = require('path');

const targetBaseDir = 'c:\\Users\\PC\\OneDrive\\Documents\\Master tool\\ai-os-v4\\phase_03_prompt_library';

const requiredSubdirs = [
  'software_engineering',
  'ai_ml',
  'web_development',
  'mobile_dev',
  'cloud_devops',
  'cybersecurity',
  'data_engineering',
  'architecture_design',
  'quality_assurance',
  'documentation',
  'mechanical_engineering',
  'manufacturing',
  'construction',
  'finance',
  'legal',
  'marketing',
  'healthcare',
  'education',
  'agriculture',
  'supply_chain'
];

const requiredFiles = [
  'system.md',
  'planning.md',
  'review.md',
  'verification.md',
  'optimization.md',
  'domain_workflow_prompt.md'
];

console.log("=== VERIFYING PHASE 03 PROMPT LIBRARY ===");

let errors = [];
let fileCount = 0;
let minWords = Infinity;
let maxWords = 0;
let totalWords = 0;

if (!fs.existsSync(targetBaseDir)) {
  errors.push(`Target directory does not exist: ${targetBaseDir}`);
} else {
  const actualSubdirs = fs.readdirSync(targetBaseDir).filter(f => fs.statSync(path.join(targetBaseDir, f)).isDirectory());

  // Check subdirs count
  if (actualSubdirs.length !== requiredSubdirs.length) {
    errors.push(`Subdirectory count mismatch: expected ${requiredSubdirs.length}, got ${actualSubdirs.length}`);
  }

  requiredSubdirs.forEach(subdir => {
    const dirPath = path.join(targetBaseDir, subdir);
    if (!fs.existsSync(dirPath)) {
      errors.push(`Missing domain subdirectory: ${subdir}`);
      return;
    }

    requiredFiles.forEach(file => {
      const filePath = path.join(dirPath, file);
      if (!fs.existsSync(filePath)) {
        errors.push(`Missing file: ${subdir}/${file}`);
      } else {
        fileCount++;
        const content = fs.readFileSync(filePath, 'utf8');
        const words = content.trim().split(/\s+/).length;
        
        if (words < 200) {
          errors.push(`File ${subdir}/${file} has only ${words} words (minimum 200 required)`);
        }

        if (!content.includes('{input}')) {
          errors.push(`File ${subdir}/${file} missing {input} variable`);
        }

        if (words < minWords) minWords = words;
        if (words > maxWords) maxWords = words;
        totalWords += words;
      }
    });
  });
}

console.log(`Total files verified: ${fileCount} / ${requiredSubdirs.length * requiredFiles.length}`);
console.log(`Word Count Stats - Min: ${minWords}, Max: ${maxWords}, Avg: ${Math.round(totalWords / (fileCount || 1))}`);

if (errors.length === 0) {
  console.log("VERIFICATION SUCCESS: All 120 files across 20 domain subdirectories verified successfully!");
  process.exit(0);
} else {
  console.error(`VERIFICATION FAILED: ${errors.length} errors found:`);
  errors.forEach(err => console.error(` - ${err}`));
  process.exit(1);
}
