A parser that will take a PDF of a USP monograph and return a excel compatible file with step by step instructions for the requested test.

PDF files of the monograph of interest will be converted to text using pypdf, the text object is then converted into a python dict. The dict
is of {SECTION: body text} form where SECTION is one of "DEFINITION", "IDENTIFICATION", "ASSAY", "IMPURITIES", "PERFORMANCE TESTS", "SPECIFIC TESTS",
"ADDITIONAL REQUIREMENTS".

The resulting dict object is used to target sections for further refinement or for feeding the body text through a LLM to generate a step by step list
with instructions for completing the testing, i.e. solution preps. This list will be used to populate the excel compatible file.

A small flask app is used as the interface to allow for drag and drop file selection. After connecting to the flask app through the browser, the pdf can be
drag and dropped. After processing is complete the .xlsx file is downloaded by the client. 




