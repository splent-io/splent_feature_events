// Entry point for splent_feature_events frontend assets.
// Add your JavaScript here. Webpack compiles this into assets/dist/splent_feature_events.bundle.js
//
// To load the compiled bundle in the product layout, register it in hooks.py:
//
//   from splent_framework.hooks.template_hooks import register_template_hook
//   from flask import url_for
//
//   def events_scripts():
//       return '<script src="' + url_for("events.assets", subfolder="dist", filename="splent_feature_events.bundle.js") + '"></script>'
//
//   register_template_hook("layout.scripts", events_scripts)
