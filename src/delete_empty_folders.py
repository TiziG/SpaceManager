import space_manager

# configuration-----------
TEST_RUN = False
LOGGING = True
# ------------------------

space_manager.delete_empty_folders(test_run=TEST_RUN, logging=LOGGING)
