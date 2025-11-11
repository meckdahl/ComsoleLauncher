#!/usr/bin/env python3
"""
Simple MPH Library Example
Demonstrates basic Comsol control using the mph Python library

Based on YouTube tutorial about Comsol control with Python
Source: https://www.youtube.com/watch?v=... (Comsol Python Control)

This script shows the fundamental workflow:
1. Connect to Comsol server
2. Load a model
3. View/modify parameters
4. Build and solve
5. Export results
"""

import mph
import numpy as np
from pathlib import Path
import sys


def main():
    """Main demonstration function"""
    
    print("=" * 60)
    print("MPH Library - Simple Comsol Control Example")
    print("=" * 60)
    
    # ========================================
    # STEP 1: Connect to Comsol Server
    # ========================================
    print("\n[1] Connecting to Comsol server...")
    
    try:
        client = mph.start()
        print("✓ Connected successfully")
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        print("\nTroubleshooting:")
        print("  - Ensure Comsol Multiphysics is installed")
        print("  - Check that Java is available (java -version)")
        print("  - Try: pip install --upgrade mph")
        sys.exit(1)
    
    # ========================================
    # STEP 2: Load a Model
    # ========================================
    print("\n[2] Loading Comsol model...")
    
    # You need to specify your model file path
    model_path = "Model_name.mph"  # Change this to your model
    
    # Check if file exists
    if not Path(model_path).exists():
        print(f"✗ Model file not found: {model_path}")
        print("\nNote: This is a demonstration script.")
        print("To use it, replace 'Model_name.mph' with your actual model file.")
        print("\nExample:")
        print('  model = client.load("path/to/your/model.mph")')
        
        # Show what we would do if model existed
        print("\n" + "=" * 60)
        print("DEMONSTRATION: What would happen with a real model...")
        print("=" * 60)
        demonstrate_workflow()
        sys.exit(0)
    
    try:
        model = client.load(model_path)
        print(f"✓ Model loaded: {model_path}")
    except Exception as e:
        print(f"✗ Failed to load model: {str(e)}")
        sys.exit(1)
    
    # ========================================
    # STEP 3: View Parameters
    # ========================================
    print("\n[3] Reading model parameters...")
    
    try:
        params = model.parameters()
        print(f"✓ Found {len(params)} parameters:")
        
        for param_name, param_value in params.items():
            print(f"   {param_name}: {param_value}")
    
    except Exception as e:
        print(f"✗ Failed to read parameters: {str(e)}")
    
    # ========================================
    # STEP 4: Modify a Parameter
    # ========================================
    print("\n[4] Modifying parameter...")
    
    # Example: Change voltage parameter
    # Modify this based on your model's parameters
    param_to_change = "Voltage"  # Change this to match your parameter
    new_value = "20"  # New value with units if needed
    
    if param_to_change in params:
        try:
            model.parameter(param_to_change, new_value)
            print(f"✓ Set {param_to_change} = {new_value}")
        except Exception as e:
            print(f"✗ Failed to set parameter: {str(e)}")
    else:
        print(f"⚠ Parameter '{param_to_change}' not found in model")
        print(f"  Available parameters: {list(params.keys())}")
    
    # ========================================
    # STEP 5: Build Model
    # ========================================
    print("\n[5] Building model...")
    
    try:
        model.build()
        print("✓ Model built successfully")
    except Exception as e:
        print(f"✗ Build failed: {str(e)}")
        sys.exit(1)
    
    # ========================================
    # STEP 6: Solve Model
    # ========================================
    print("\n[6] Solving model (this may take time)...")
    
    try:
        model.solve()
        print("✓ Solution completed")
    except Exception as e:
        print(f"✗ Solution failed: {str(e)}")
        sys.exit(1)
    
    # ========================================
    # STEP 7: Save Results
    # ========================================
    print("\n[7] Saving results...")
    
    output_name = f"Save_name.mph"  # Customize as needed
    
    try:
        model.save(output_name)
        print(f"✓ Results saved: {output_name}")
    except Exception as e:
        print(f"✗ Save failed: {str(e)}")
    
    print("\n" + "=" * 60)
    print("COMPLETE - Model processed successfully!")
    print("=" * 60)


def demonstrate_workflow():
    """
    Demonstrate the workflow without actually running Comsol
    Used when model file is not available
    """
    
    print("\n1. Connect to Comsol:")
    print("   client = mph.start()")
    
    print("\n2. Load model:")
    print("   model = client.load('Model_name.mph')")
    
    print("\n3. View parameters:")
    print("   params = model.parameters()")
    print("   # Output: {'Voltage': '1', 'Current': '0.5', ...}")
    
    print("\n4. Modify parameter:")
    print("   model.parameter('Voltage', '20')")
    
    print("\n5. Build model:")
    print("   model.build()")
    
    print("\n6. Solve:")
    print("   model.solve()")
    
    print("\n7. Save results:")
    print("   model.save('Model_solved.mph')")
    
    print("\n" + "=" * 60)
    print("ADVANCED USAGE")
    print("=" * 60)
    
    print("\nParameter sweep example:")
    print("""
    for voltage in range(2, 12, 2):
        model.parameter('Voltage', str(voltage))
        model.build()
        model.solve()
        model.save(f'Model_V{voltage}.mph')
        print(f'Completed: V={voltage}')
    """)
    
    print("\nExtract specific data:")
    print("""
    # Get data at specific coordinates
    data = model.evaluate('V', '0', '0')
    
    # Process with numpy
    max_voltage = np.max(data)
    print(f'Maximum voltage: {max_voltage}')
    """)
    
    print("\nExport images:")
    print("""
    model.export('image1', 'result_plot.png')
    """)


def batch_parameter_sweep_example():
    """
    Example of running multiple simulations with different parameters
    (From the YouTube tutorial)
    """
    
    print("\n" + "=" * 60)
    print("BATCH PROCESSING EXAMPLE")
    print("=" * 60)
    
    example_code = '''
import mph
import numpy as np

# Connect and load
client = mph.start()
model = client.load("Model_name.mph")

# Define parameter range
V_min = 2
V_max = 10

# Run simulations for each voltage
for voltage in range(V_min, V_max + 1):
    print(f"Processing: Voltage = {voltage}V")
    
    # Set parameter
    model.parameter("Voltage", str(voltage))
    
    # Build and solve
    model.build()
    model.solve()
    
    # Calculate maximum voltage in domain
    data = model.evaluate("V", "0", "0")
    V_max_calc = np.max(data)
    print(f"  Maximum voltage: {V_max_calc:.2f}V")
    
    # Export plot
    model.export("image1", f"V_solved_{voltage}V.png")
    
    # Save model
    model.save(f"V_solved_{voltage}V.mph")
    
print("Batch processing complete!")
'''
    
    print(example_code)


if __name__ == "__main__":
    main()
    
    # Uncomment to see batch processing example
    # batch_parameter_sweep_example()
