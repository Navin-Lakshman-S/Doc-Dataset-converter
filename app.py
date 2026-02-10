"""
AI Data Conversion Tool - Main Application
A universal file-to-dataset converter for AI training
"""
import gradio as gr
import os
import json
import tempfile
from typing import Dict, Any, List, Tuple
import shutil

# Import converters
from converters.pdf_converter import PDFConverter
from converters.word_converter import WordConverter
from converters.excel_converter import ExcelConverter
from converters.text_converter import TextConverter

# Import utilities
from utils.cleaner import DataCleaner
from utils.formatter import DataFormatter
from utils.validator import FileValidator


class AIDataConverter:
    """Main application class for AI Data Conversion Tool"""
    
    def __init__(self):
        self.output_dir = "output"
        self._ensure_output_dir()
        self.cleaner = DataCleaner()
        self.formatter = DataFormatter()
        self.validator = FileValidator()
    
    def _ensure_output_dir(self):
        """Ensure output directory exists"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def process_file(
        self,
        file_path: str,
        output_format: str,
        clean_text: bool,
        remove_urls: bool,
        remove_extra_spaces: bool,
        lowercase: bool
    ) -> Tuple[str, str, str, str]:
        """
        Process a single file and return results
        
        Returns:
            Tuple of (status_message, preview_json, download_path, statistics)
        """
        try:
            # Validate file
            is_valid, validation_msg = self.validator.validate_file(file_path)
            if not is_valid:
                return validation_msg, "", None, ""
            
            # Extract data based on file type
            ext = os.path.splitext(file_path)[1].lower()
            
            if ext == '.pdf':
                converter = PDFConverter(file_path)
            elif ext in ['.docx', '.doc']:
                converter = WordConverter(file_path)
            elif ext in ['.xlsx', '.xls']:
                converter = ExcelConverter(file_path)
            elif ext in ['.txt', '.csv']:
                converter = TextConverter(file_path)
            else:
                return f"Unsupported file type: {ext}", "", None, ""
            
            # Extract data
            extracted_data = converter.extract()
            
            if "error" in extracted_data:
                return extracted_data["error"], "", None, ""
            
            # Clean data if requested
            if clean_text and "full_text" in extracted_data:
                cleaning_options = {
                    'remove_extra_spaces': remove_extra_spaces,
                    'remove_urls': remove_urls,
                    'lowercase': lowercase,
                    'remove_special_chars': False,
                    'remove_numbers': False
                }
                extracted_data["full_text"] = self.cleaner.clean_text(
                    extracted_data["full_text"], 
                    cleaning_options
                )
            
            # Generate statistics
            stats = self.formatter.get_statistics(extracted_data)
            stats_text = self._format_statistics(stats)
            
            # Format output
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            
            if output_format == "JSON":
                output_path = os.path.join(self.output_dir, f"{base_name}_converted.json")
                json_output = self.formatter.to_json(extracted_data)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(json_output)
                
                preview = json_output[:2000] + "..." if len(json_output) > 2000 else json_output
                
            elif output_format == "CSV":
                output_path = os.path.join(self.output_dir, f"{base_name}_converted.csv")
                
                # Extract tabular data for CSV
                csv_data = self._extract_tabular_data(extracted_data)
                if csv_data:
                    self.formatter.to_csv(csv_data, output_path)
                    preview = f"CSV file created with {len(csv_data)} rows"
                else:
                    return "No tabular data found for CSV export", "", None, stats_text
                
            elif output_format == "XML":
                output_path = os.path.join(self.output_dir, f"{base_name}_converted.xml")
                xml_output = self.formatter.to_xml(extracted_data)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(xml_output)
                
                preview = xml_output[:2000] + "..." if len(xml_output) > 2000 else xml_output
            
            elif output_format == "AI Training Format":
                output_path = os.path.join(self.output_dir, f"{base_name}_ai_training.json")
                ai_format = self.formatter.create_ai_training_format(extracted_data)
                json_output = self.formatter.to_json(ai_format)
                
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(json_output)
                
                preview = json_output[:2000] + "..." if len(json_output) > 2000 else json_output
            
            success_msg = f"Successfully processed: {os.path.basename(file_path)}\nOutput saved to: {output_path}"
            
            return success_msg, preview, output_path, stats_text
            
        except Exception as e:
            return f"Error processing file: {str(e)}", "", None, ""
    
    def _extract_tabular_data(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract tabular data from extracted content"""
        if "data" in data:
            return data["data"]
        elif "all_data" in data:
            return data["all_data"]
        elif "tables" in data and data["tables"]:
            # Convert first table to list of dicts
            first_table = data["tables"][0]["data"]
            if first_table and len(first_table) > 1:
                headers = first_table[0]
                rows = first_table[1:]
                return [dict(zip(headers, row)) for row in rows]
        return []
    
    def _format_statistics(self, stats: Dict[str, Any]) -> str:
        """Format statistics for display"""
        output = "**Document Statistics**\n\n"
        
        for key, value in stats.items():
            formatted_key = key.replace('_', ' ').title()
            output += f"**{formatted_key}:** {value}\n"
        
        return output
    
    def process_batch(
        self,
        files: List[Any],
        output_format: str,
        clean_text: bool,
        remove_urls: bool,
        remove_extra_spaces: bool,
        lowercase: bool
    ) -> Tuple[str, str]:
        """Process multiple files in batch"""
        if not files:
            return "No files uploaded", ""
        
        results = []
        successful = 0
        failed = 0
        
        for file_obj in files:
            file_path = file_obj.name
            status, _, output_path, _ = self.process_file(
                file_path,
                output_format,
                clean_text,
                remove_urls,
                remove_extra_spaces,
                lowercase
            )
            
            if output_path:
                successful += 1
                results.append(f"[OK] {os.path.basename(file_path)}")
            else:
                failed += 1
                results.append(f"[FAILED] {os.path.basename(file_path)}: {status}")
        
        summary = f"**Batch Processing Complete**\n\n"
        summary += f"Successful: {successful}\n"
        summary += f"Failed: {failed}\n\n"
        summary += "**Details:**\n" + "\n".join(results)
        
        # Create a zip file with all outputs
        if successful > 0:
            zip_path = os.path.join(self.output_dir, "batch_output.zip")
            shutil.make_archive(
                os.path.join(self.output_dir, "batch_output"),
                'zip',
                self.output_dir
            )
            return summary, zip_path
        
        return summary, None


# Create the Gradio interface
def create_interface():
    """Create and configure the Gradio interface"""
    
    app = AIDataConverter()
    
    # Custom CSS for better styling
    custom_css = """
    .primary-btn {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%) !important;
        border: none !important;
    }
    .output-box {
        border: 2px solid #4CAF50 !important;
        border-radius: 8px !important;
    }
    .hero-section {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
    .stat-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        margin: 10px;
    }
    """
    
    with gr.Blocks(
        title="AI Data Conversion Tool",
        theme=gr.themes.Soft(primary_hue="green"),
        css=custom_css
    ) as interface:
        
        with gr.Tabs():
            # Landing Page Tab
            with gr.Tab("Home"):
                # Hero Section
                gr.Markdown(
                    """
                    <div style="text-align: center; padding: 60px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white; margin-bottom: 30px;">
                        <h1 style="font-size: 3em; margin-bottom: 10px;">Document to Dataset Converter</h1>
                        <h2 style="font-size: 1.5em; font-weight: 300; margin-bottom: 20px;">Turn your PDFs, Word docs, and spreadsheets into clean data for AI training</h2>
                        <p style="font-size: 1.2em; max-width: 800px; margin: 0 auto;">
                            Built this because manually copying data from documents takes forever. 
                            Now it takes a few seconds instead of hours.
                        </p>
                    </div>
                    """
                )
                
                # Key Stats
                with gr.Row():
                    with gr.Column():
                        gr.Markdown(
                            """
                            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 10px; text-align: center;">
                                <h2 style="font-size: 2.5em; margin: 0;">7+</h2>
                                <p style="margin: 10px 0 0 0;">File types supported</p>
                            </div>
                            """
                        )
                    with gr.Column():
                        gr.Markdown(
                            """
                            <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; border-radius: 10px; text-align: center;">
                                <h2 style="font-size: 2.5em; margin: 0;">~2 sec</h2>
                                <p style="margin: 10px 0 0 0;">Average processing time</p>
                            </div>
                            """
                        )
                    with gr.Column():
                        gr.Markdown(
                            """
                            <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 30px; border-radius: 10px; text-align: center;">
                                <h2 style="font-size: 2.5em; margin: 0;">Batch</h2>
                                <p style="margin: 10px 0 0 0;">Process multiple files</p>
                            </div>
                            """
                        )
                    with gr.Column():
                        gr.Markdown(
                            """
                            <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 30px; border-radius: 10px; text-align: center;">
                                <h2 style="font-size: 2.5em; margin: 0;">Free</h2>
                                <p style="margin: 10px 0 0 0;">No subscriptions</p>
                            </div>
                            """
                        )
                
                gr.Markdown("<br>")
                
                # Features Section
                gr.Markdown("## What it does")
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown(
                            """
                            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 4px solid #667eea; margin: 10px 0;">
                                <h3>Works with most file types</h3>
                                <p>PDF, Word docs, Excel files, plain text, CSV - basically anything you'd normally have to copy-paste from.</p>
                            </div>
                            """
                        )
                        gr.Markdown(
                            """
                            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 4px solid #f5576c; margin: 10px 0;">
                                <h3>Extracts tables automatically</h3>
                                <p>Finds tables in PDFs and Word documents. No more manually recreating spreadsheets from screenshots.</p>
                            </div>
                            """
                        )
                    
                    with gr.Column():
                        gr.Markdown(
                            """
                            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 4px solid #00f2fe; margin: 10px 0;">
                                <h3>Upload multiple files at once</h3>
                                <p>Got 50 invoices to process? Upload them all together. Way faster than doing them one by one.</p>
                            </div>
                            """
                        )
                        gr.Markdown(
                            """
                            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 4px solid #38f9d7; margin: 10px 0;">
                                <h3>Cleans up messy text</h3>
                                <p>Removes page numbers, headers, extra spaces - all the annoying stuff you'd have to clean manually.</p>
                            </div>
                            """
                        )
                
                with gr.Row():
                    with gr.Column():
                        gr.Markdown(
                            """
                            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 4px solid #43e97b; margin: 10px 0;">
                                <h3>Export in different formats</h3>
                                <p>Get your data as JSON, CSV, or XML. Whatever works best for your project.</p>
                            </div>
                            """
                        )
                    with gr.Column():
                        gr.Markdown(
                            """
                            <div style="background: #f8f9fa; padding: 25px; border-radius: 10px; border-left: 4px solid #764ba2; margin: 10px 0;">
                                <h3>Preview before downloading</h3>
                                <p>Check if the extraction looks good before saving. No surprises.</p>
                            </div>
                            """
                        )
                
                gr.Markdown("<br>")
                
                # Use Cases
                gr.Markdown("## Who uses this?")
                
                with gr.Row():
                    gr.Markdown(
                        """
                        <div style="background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 10px;">
                            <h4>Legal teams</h4>
                            <p>Converting hundreds of contracts and agreements into searchable databases.</p>
                        </div>
                        """
                    )
                    gr.Markdown(
                        """
                        <div style="background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 10px;">
                            <h4>Researchers</h4>
                            <p>Extracting data from papers and reports for analysis.</p>
                        </div>
                        """
                    )
                    gr.Markdown(
                        """
                        <div style="background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 10px;">
                            <h4>Data scientists</h4>
                            <p>Preparing training datasets for machine learning models.</p>
                        </div>
                        """
                    )
                    gr.Markdown(
                        """
                        <div style="background: #fff; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin: 10px;">
                            <h4>Anyone with data in docs</h4>
                            <p>If you've ever copy-pasted from PDFs, this will save you time.</p>
                        </div>
                        """
                    )
                
                gr.Markdown("<br>")
                
                # How It Works
                gr.Markdown("## How to use it")
                gr.Markdown(
                    """
                    <div style="background: #f8f9fa; padding: 30px; border-radius: 10px; margin: 20px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
                            <div style="flex: 1; min-width: 200px; text-align: center; margin: 10px;">
                                <div style="background: #667eea; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 1.5em; font-weight: bold;">1</div>
                                <h4>Upload your file</h4>
                                <p>Drop it in or click to browse</p>
                            </div>
                            <div style="flex: 0 0 50px; text-align: center; font-size: 2em; color: #667eea;">→</div>
                            <div style="flex: 1; min-width: 200px; text-align: center; margin: 10px;">
                                <div style="background: #f5576c; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 1.5em; font-weight: bold;">2</div>
                                <h4>Pick your format</h4>
                                <p>JSON, CSV, or XML</p>
                            </div>
                            <div style="flex: 0 0 50px; text-align: center; font-size: 2em; color: #f5576c;">→</div>
                            <div style="flex: 1; min-width: 200px; text-align: center; margin: 10px;">
                                <div style="background: #00f2fe; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 1.5em; font-weight: bold;">3</div>
                                <h4>Hit convert</h4>
                                <p>Takes a couple seconds</p>
                            </div>
                            <div style="flex: 0 0 50px; text-align: center; font-size: 2em; color: #00f2fe;">→</div>
                            <div style="flex: 1; min-width: 200px; text-align: center; margin: 10px;">
                                <div style="background: #38f9d7; color: white; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 1.5em; font-weight: bold;">4</div>
                                <h4>Download</h4>
                                <p>Your data is ready</p>
                            </div>
                        </div>
                    </div>
                    """
                )
                
                gr.Markdown("<br>")
                
                # Call to Action
                gr.Markdown(
                    """
                    <div style="text-align: center; padding: 50px 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
                        <h2 style="font-size: 2em; margin-bottom: 20px;">Ready to try it?</h2>
                        <p style="font-size: 1.2em; margin-bottom: 30px;">Click the "Single File Converter" or "Batch Converter" tab above to get started</p>
                    </div>
                    """
                )
                
                gr.Markdown("<br>")
                
                # Footer
                gr.Markdown(
                    """
                    <div style="text-align: center; color: #666; padding: 20px;">
                        <p>Everything runs on your machine - files aren't sent anywhere</p>
                        <p>Built with Python, PyMuPDF, Gradio, and a bunch of other open source tools</p>
                    </div>
                    """
                )
            
            # Single File Processing Tab
            with gr.Tab("Single File Converter"):
                with gr.Row():
                    with gr.Column(scale=1):
                        gr.Markdown("### Upload & Configure")
                        
                        file_input = gr.File(
                            label="Upload Document",
                            file_types=[".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"]
                        )
                        
                        output_format = gr.Radio(
                            choices=["JSON", "CSV", "XML", "AI Training Format"],
                            value="JSON",
                            label="Output Format"
                        )
                        
                        with gr.Accordion("Cleaning Options", open=False):
                            clean_text = gr.Checkbox(label="Enable Text Cleaning", value=True)
                            remove_urls = gr.Checkbox(label="Remove URLs", value=True)
                            remove_extra_spaces = gr.Checkbox(label="Remove Extra Spaces", value=True)
                            lowercase = gr.Checkbox(label="Convert to Lowercase", value=False)
                        
                        process_btn = gr.Button("Convert to Dataset", variant="primary")
                    
                    with gr.Column(scale=1):
                        gr.Markdown("### Results & Preview")
                        
                        status_output = gr.Textbox(
                            label="Status",
                            lines=3,
                            interactive=False
                        )
                        
                        stats_output = gr.Markdown(label="Statistics")
                        
                        preview_output = gr.Code(
                            label="Data Preview",
                            language="json",
                            lines=15
                        )
                        
                        download_output = gr.File(label="Download Converted File")
                
                process_btn.click(
                    fn=app.process_file,
                    inputs=[
                        file_input,
                        output_format,
                        clean_text,
                        remove_urls,
                        remove_extra_spaces,
                        lowercase
                    ],
                    outputs=[status_output, preview_output, download_output, stats_output]
                )
            
            # Batch Processing Tab
            with gr.Tab("Batch Converter"):
                gr.Markdown("### Upload multiple files for batch processing")
                
                with gr.Row():
                    with gr.Column():
                        batch_files = gr.File(
                            label="Upload Multiple Documents",
                            file_count="multiple",
                            file_types=[".pdf", ".docx", ".xlsx", ".xls", ".txt", ".csv"]
                        )
                        
                        batch_output_format = gr.Radio(
                            choices=["JSON", "CSV", "XML", "AI Training Format"],
                            value="JSON",
                            label="Output Format"
                        )
                        
                        with gr.Accordion("Cleaning Options", open=False):
                            batch_clean = gr.Checkbox(label="Enable Text Cleaning", value=True)
                            batch_remove_urls = gr.Checkbox(label="Remove URLs", value=True)
                            batch_remove_spaces = gr.Checkbox(label="Remove Extra Spaces", value=True)
                            batch_lowercase = gr.Checkbox(label="Convert to Lowercase", value=False)
                        
                        batch_process_btn = gr.Button("Process Batch", variant="primary")
                    
                    with gr. Column():
                        batch_status = gr.Markdown(label="Batch Results")
                        batch_download = gr.File(label="Download All Files (ZIP)")
                
                batch_process_btn.click(
                    fn=app.process_batch,
                    inputs=[
                        batch_files,
                        batch_output_format,
                        batch_clean,
                        batch_remove_urls,
                        batch_remove_spaces,
                        batch_lowercase
                    ],
                    outputs=[batch_status, batch_download]
                )
            
            # Documentation Tab
            with gr.Tab("Documentation"):
                gr.Markdown(
                    """
                    ## About this tool
                    
                    This tool converts documents into structured data. If you've ever needed to get data out of PDFs,
                    Word files, or spreadsheets for machine learning, this is for you.
                    
                    ### What it can do
                    
                    - Works with PDF, Word, Excel, text, and CSV files
                    - Can process multiple files at once
                    - Automatically finds and extracts tables
                    - Removes common junk (page numbers, headers, URLs)
                    - Exports to JSON, CSV, or XML
                    - Shows you a preview before you download
                    
                    ### How to use it
                    
                    1. Upload your document(s)
                    2. Pick an output format (JSON is usually good)
                    3. Click convert - usually takes 2-3 seconds
                    4. Download your file
                    
                    ### When you might need this
                    
                    - You have data locked in PDFs or Word docs
                    - You need to train a machine learning model
                    - You're doing research and need to extract info from papers
                    - You have a bunch of invoices/reports to process
                    - You're tired of copy-pasting from documents
                    
                    ### Output formats explained
                    
                    **JSON** - Most versatile. Works with pretty much any programming language or tool.
                    
                    **CSV** - Good if your data is table-like (like an Excel sheet). Opens in Excel/Google Sheets.
                    
                    **XML** - If you need hierarchical data or your system requires XML specifically.
                    
                    **AI Training Format** - Special format that includes the text plus metadata. 
                    Useful if you're training language models or doing NLP.
                    
                    ### What powers this
                    
                    Built with Python using PyMuPDF and pdfplumber for PDFs, python-docx for Word files,
                    and pandas for Excel. The interface is Gradio.
                    
                    All processing happens on your computer - nothing gets sent to external servers.
                    """
                )
        
        gr.Markdown(
            """
            ---
            <div style="text-align: center; color: #666;">
                <p><b>Note:</b> Password-protected files won't work. Max file size is 50MB.</p>
            </div>
            """
        )
    
    return interface


# Main execution
if __name__ == "__main__":
    interface = create_interface()
    interface.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )
