import pandas as pd

# Recreate the original list after code execution reset
technical_verbs = [
    "Adapted", "Architected", "Augmented", "Batched", "Built-in", "Cached", "Centralized", "Circulated",
    "Cloned", "Clustered", "Coordinated", "Corrected", "Customized", "Debugged", "Decoded", "Decommissioned",
    "Deconstructed", "Defined", "Delegated", "Derived", "Designed", "Detected", "Diagnosed", "Differentiated",
    "Diminished", "Directed", "Dissected", "Downgraded", "Drilled-down", "Embedded", "Emulated", "Encoded",
    "Enforced", "Enlisted", "Enumerated", "Escalated", "Established", "Executed", "Expanded", "Explored",
    "Extended", "Extracted", "Finalized", "Flagged", "Formatted", "Formulated", "Generated", "Graphically-modeled",
    "Groomed", "Handled", "Hardened", "Implemented", "Imported", "Improved", "Indexed", "Indicated", "Influenced",
    "Injected", "Inspected", "Instrumented", "Interfaced", "Interlinked", "Isolated", "Laid out", "Logged",
    "Maintained", "Manipulated", "Mapped out", "Measured", "Mocked", "Monitored", "Normalized", "Observed",
    "Parsed", "Partitioned", "Patched", "Performed", "Pipelined", "Planned", "Populated", "Predicted",
    "Preprocessed", "Prioritized", "Processed", "Probed", "Programmed", "Provisioned", "Published", "Queried",
    "Reallocated", "Reapplied", "Refactored", "Refined", "Refreshed", "Registered", "Reindexed", "Reorganized",
    "Repurposed", "Rescaled", "Restructured", "Retested", "Routed", "Sanitized", "Scaled", "Scripted", "Secured",
    "Segmented", "Simulated", "Simplified", "Snapped", "Streamlined", "Synchronized", "Templated", "Troubleshot",
    "Tuned", "Validated", "Versioned", "Visualized"
]

# Additional power verbs from user
# Obtained from https://www.dice.com/career-advice/power-verbs-for-technical-work
additional_verbs_str = """
Accelerated,Deployed,Merged,Refreshed,Added,Digitized,Migrated,Reinforced,Adopted,Discovered,Mined,
Rehabilitated,Aggregated,Dispatched,Mirrored,Released,Analyzed,Distributed,Mobilized,Remodeled,Applied,
Duplicated,Modeled,Replicated,Assembled,Enabled,Modified,Restored,Assessed,Engineered,Moved,Retooled,
Authenticated,Enhanced,Networked,Retrieved,Automated,Eradicated,Neutralized,Retrofitted,Backed‑up,
Estimated,Onboarded,Revamped,Balanced,Equipped,Operated,Road mapped,Blocked,Evaluated,Optimized,
Rolled out,Boosted,Expunged,Orchestrated,Rotated,Branched,Extended,Overhauled,Routed,Bridged,Extracted,
Packaged,Safeguarded,Built,Extrapolated,Patched,Salvaged,Bundled,Fabricated,Penetrated,Scanned,
Calculated,Facilitated,Pinpointed,Scoped,Calibrated,Finalized,Presented,Scrubbed,Certified,Fine‑Tuned,
Prevented,Secured,Changed,Formatted,Prioritized,Selected,Checked,Founded,Processed,Sequenced,
Classified,Functionalized,Programmed,Solved,Cleaned,Grouped,Proposed,Stabilized,Cleansed,Hosted,
Protected,Standardized,Cleared,Identified,Prototyped,Straddled,Coded,Implemented,Provisioned,
Spearheaded,Collocated,Increased,Qualified,Systematized,Computed,Initiated,Quality Assured,Tested,
Computerized,Installed,Ranked,Toggled,Configured,Integrated,Realigned,Traced,Consolidated,Isolated,
Rebooted,Transitioned,Constructed,Launched,Rebuilt,Updated,Corrected,Licensed,Reconciled,Upgraded,
Debugged,Linked,Reconstructed,Validated,Deciphered,Loaded,Recovered,Verified,Decoded,Maintained,
Rectified,Virtualized,Dedicated,Manufactured,Reduced,Web‑enabled,Defended,Mapped,Re‑engineered,
Wrangled,Delivered,Mechanized
"""

# The following was obtained through https://careers.uiowa.edu/resume-writing-power-verbs
planning_verbs = """
Commissioned,Developed,Evaluated,Formulated,Observed,Prepared,Researched,Revised,Studied,
Anticipated,Determined,Devised,Forecasted,Identified,Planned,Prioritized,Reserved,Strategized,Tailored
"""
organizational_verbs = """
Acquired,Appointed,Authorized,Collected,Customized,Facilitated,Issued,Ordered,Retrieved,Simplified,
Activated,Arranged,Catalogued,Committed,Delegated,Housed,Linked,Organized,Routed,Sought,Adjusted,
Assembled,Centralized,Confirmed,Designated,Implemented,Logged,Procured,Scheduled,Straightened,Allocated,
Assessed,Charted,Contracted,Designed,Incorporated,Mapped,out,Programmed,Secured,Suggested,Altered,Assigned,
Classified,Coordinated,Established,Instituted,Obtained,Recruited,Selected,Tracked"""

executing_verbs = """Acted,Collected,Displayed,Exercised,Input,Merchandised,Produced,Proved,Sold,Administered,
Completed,Distributed,Forwarded,Installed,Operated,Proofed,Performed,Stocked,Carried,out,Conducted,Entered,Handled,
Labored,Processed,Prospected,Shipped,Transacted"""

supervising_verbs = """Adjusted,Certified,Correlated,Examined,Indexed,Measured,Overhauled,Refined,Screened,Supplied,
Analyzed,Compared,Developed,Explored,Judged,Modified,Oversaw,Regulated,Set,Tightened,Apportioned,Controlled,Discovered,
Graded,Licensed,Monitored,Policed,Reviewed,Scrutinized,Traced,Assessed,Corrected,Established,Inspected,Maintained,Officiated,
Prohibited,Revised,Supervised,Updated"""

leading_verbs = """Accelerated,Changed,Elected,Encouraged,Founded,Inspired,Mentored,Promoted,Spearheaded,Assumed,Conducted,
Employed,Enlisted,Guided,Involved,Motivated,Raised,Stimulated,Caused,Directed,Hired,Envisioned,Influenced,Led,Originated,
Recognized,for,Strengthened,Chaired,Disproved,Empowered,Fostered,Initiated,Managed,Pioneered,Set,goals,Supervised"""

getting_results_verbs = """Accomplished,Boosted,Contributed,Eliminated,Expanded,Generated,Increased,Launched,Orchestrated,
Received,Achieved,Built,Delivered,Enlarged,Expedited,Grew,Innovated,Lightened,Overcame,Reduced,Added,Combined,Demonstrated,
Enjoyed,Extended,Guaranteed,Integrated,Minimized,Prevailed,Rejuvenated,Advanced,Completed,Diminished,Enlisted,Finalized,Hastened,
Introduced,Modernized,Produced,Renovated,Attained,Consolidated,Earned,Ensured,Fulfilled,Heightened,Invented,Obtained,Qualified,
Restored,Augmented,Constructed,Eclipsed,Excelled,Gained,Improved,Joined,Opened,Realized,Targeted"""

problem_solving_verbs = """Alleviated,Collaborated,Created,Detected,Foresaw,Investigated,Repaired,Revived,Synthesized,Analyzed,
Conceived,Debugged,Determined,Formulated,Recommended,Resolved,Satisfied,Theorized,Applied,Conceptualized,Decided,Diagnosed,Found,Remedied,Revamped,
Solved,Brainstormed,Crafted,Deciphered,Engineered,Gathered,Remodeled,Revitalized,Streamlined"""

quantitative_verbs = """Accounted,for,Balanced,Compiled,Converted,Earned,Financed,Maximized,Projected,Reconciled,Totaled,Appraised,Budgeted,
Compounded,Counted,Enumerated,Grossed,Multiplied,Purchased,Recorded,Approximated,Calculated,Computed,Dispensed,Estimated,Increased,Netted,Quantified,
Reduced,Audited,Checked,Conserved,Dispersed,Figured,Inventoried,Profited,Rated,Tabulated"""

communicating_verbs = """Acted,Attested,Convinced,Dramatized,Highlighted,Justified,Publicized,Revealed,Submitted,Tested,Adapted,Briefed,Consulted,Edited,
Illustrated,Lectured,Queried,Sanctioned,Substantiated,Taught,Admitted,Clarified,Corresponded,Educated,Improvised,Marketed,Questioned,Settled,Suggested,
Translated,Addressed,Cleared,Up,Critiqued,Elicited,Indicated,Mediated,Referred,Shaped,Summarized,Transmitted,Allowed,Closed,Dedicated,Explained,Inferred,
Moderated,Reinforced,Smoothed,Supplemented,Verified,Amended,Communicated,Defined,Extracted,Informed,Negotiated,Related,Specified,Supported,Welcomed,Arbitrated,
Composed,Deliberated,Fabricated,Instructed,Perceived,Rendered,Spoke,Surveyed,Wrote,Argued,Consented,Demonstrated,Fashioned,Interpreted,Persuaded,Reported,Sold,
Synthesized,Ascertained,Concluded,Drafted,Greeted,Interviewed,Presented,Represented,Solicited,Systematized"""

helping_verbs = """Aided,Assisted,Continued,Eased,Enhanced,Interceded,Prescribed,Rescued,Sustained,Accommodated,Assured,Cooperated,Elevated,Enriched,Mobilized,Provided,
Returned,Tutored,Advised,Bolstered,Counseled,Enabled,Familiarized,Modeled,Rehabilitated,Saved,Validated,Alleviated,Coached,Dealt,Endorsed,Helped,
Polished,Relieved,Served"""

# Process and combine lists
additional_verbs = [v.strip() for v in additional_verbs_str.split(",") if v.strip()]
combined_verbs = sorted(set(technical_verbs + additional_verbs))

# Create DataFrame and save
df_combined = pd.DataFrame(combined_verbs, columns=["Technical Verbs"])
file_path = "data/combined_technical_verbs.csv"
df_combined.to_csv(file_path, index=False)

file_path
